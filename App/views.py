from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from App.models import Banner, About, GalleryItem, NewsletterSubscriber, StudentApplication, OTPVerification, generate_otp, generate_random_password
import hashlib
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.http import JsonResponse
from .models import NewsUpdate
from .models import FeeStructure
import re
from App.forms import StudentRegistrationForm
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login


def home(request):
    news_updates = NewsUpdate.objects.filter(is_active=True)
    banner_images = list(Banner.objects.all())
    gallery_items = list(GalleryItem.objects.all()[:6])
    facilities = [
        ['Football & Cricket Field', 'Badminton Court'],
        ['Basketball Court', 'Library'],
        ['Auditoriums', 'Science Lab'],
        ['IT LAB', 'Music Room'],
    ]
    return render(request, 'index.html', {
        'banner_images': banner_images,
        'gallery_items': gallery_items,
        'facilities': facilities,
        'news_updates': news_updates,
    })


def about_view(request):
    about = list(About.objects.all())
    return render(request, 'about.html', {'about': about})


def error_404(request, exception=None):
    return render(request, 'error-404.html', status=404)


def contact(request):
    if request.method == 'POST':

        # Honeypot
        if request.POST.get('website', ''):
            return render(request, 'contact.html', {'success': True})

        name    = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        email   = request.POST.get('email', '').strip()
        need    = request.POST.get('need', '').strip()
        message = request.POST.get('message', '').strip()

        # Duplicate submission guard
        submission_key = hashlib.md5(
            f"{name}{surname}{email}{need}{message}".encode()
        ).hexdigest()
        cache_key = f"contact_form_{submission_key}"

        if cache.get(cache_key):
            return render(request, 'contact.html', {'success': True})
        cache.set(cache_key, True, 30)

        # Validation
        errors = {}
        if not name:
            errors['name'] = 'First name is required.'
        if not surname:
            errors['surname'] = 'Last name is required.'
        if not email or '@' not in email:
            errors['email'] = 'A valid email is required.'
        if not need:
            errors['need'] = 'Please specify your need.'
        if not message:
            errors['message'] = 'Message is required.'

        if errors:
            cache.delete(cache_key)
            return render(request, 'contact.html', {
                'errors': errors,
                'form_data': request.POST
            })

        subject = f'New Contact Form Submission — {need}'
        body = f"""
You have received a new message from the Fatima Convent School contact form.

Name    : {name} {surname}
Email   : {email}
Need    : {need}

Message :
{message}
        """

        confirmation_html = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto; padding: 20px;">
    <div style="text-align: center; padding: 20px 0; background-color: #f8a800;">
        <img src="https://fcss-web.onrender.com/static/images/icon/school__logo-removebg-preview.png" alt="School Logo" style="height: 60px; margin-bottom: 8px;"><br>
        <h2 style="color: white; margin: 0;">Fatima Convent Senior Secondary School</h2>
        <p style="color: white; margin: 5px 0;">Fatima Nagar, Bongaon, Rangia, Assam</p>
    </div>
    <div style="padding: 30px; background-color: #fff; border: 1px solid #eee;">
        <p>Dear <strong>{name}</strong>,</p>
        <p>Thank you for contacting <strong>Fatima Convent Senior Secondary School</strong>.</p>
        <p>We have received your message regarding <strong>"{need}"</strong> and will get back to you shortly.</p>
        <div style="background-color: #f9f9f9; border-left: 4px solid #f8a800; padding: 15px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Your message:</strong></p>
            <p style="margin: 10px 0 0 0;">{message}</p>
        </div>
        <p style="color: #999; font-size: 12px;">This is an automated confirmation. Please do not reply to this email.</p>
    </div>
    <div style="text-align: center; padding: 15px; background-color: #333; color: white; font-size: 12px;">
        <p style="margin: 0;">Fatima Convent Senior Secondary School</p>
        <p style="margin: 5px 0;">📞 +91 9954950683 | ✉️ fatimaschoolrangia@gmail.com</p>
    </div>
</body>
</html>
"""

        try:
            # Setup Brevo API client
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.BREVO_API_KEY
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(configuration)
            )

            sender = {"email": settings.DEFAULT_FROM_EMAIL}

            # Email to school
            school_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": settings.SCHOOL_EMAIL}],
                sender=sender,
                reply_to={"email": email},
                subject=subject,
                text_content=body
            )
            api_instance.send_transac_email(school_email)
            print("SCHOOL EMAIL SENT SUCCESSFULLY")

            # Confirmation email to submitter
            confirm_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": email}],
                sender=sender,
                subject='We received your message — Fatima Convent School',
                html_content=confirmation_html
            )
            api_instance.send_transac_email(confirm_email)
            print("CONFIRMATION EMAIL SENT SUCCESSFULLY")

            return render(request, 'contact.html', {'success': True})

        except ApiException as e:
            import traceback
            print(f"BREVO API ERROR: {str(e)}")
            print(traceback.format_exc())
            cache.delete(cache_key)
            return render(request, 'contact.html', {
                'error': 'Something went wrong. Please try again later.',
                'form_data': request.POST
            })

        except Exception as e:
            import traceback
            print(f"EMAIL ERROR: {str(e)}")
            print(traceback.format_exc())
            cache.delete(cache_key)
            return render(request, 'contact.html', {
                'error': 'Something went wrong. Please try again later.',
                'form_data': request.POST
            })

    return render(request, 'contact.html')


def gallery(request):
    distinct_categories = GalleryItem.objects.values_list('category', flat=True).distinct()
    gallery_images = list(GalleryItem.objects.all())
    return render(request, 'gallery.html', {
        'distinct_categories': distinct_categories,
        'gallery_images': gallery_images,
    })
    
def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()

        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(email_regex, email):
            return JsonResponse({
                'status': 'error',
                'message': 'Please enter a valid email address.'
            })

        # Check if already subscribed
        if NewsletterSubscriber.objects.filter(email=email).exists():
            subscriber = NewsletterSubscriber.objects.get(email=email)
            if subscriber.is_active:
                return JsonResponse({
                    'status': 'error',
                    'message': 'This email is already subscribed!'
                })
            else:
                # Reactivate if they had unsubscribed
                subscriber.is_active = True
                subscriber.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Welcome back! You have been resubscribed.'
                })

        # Save new subscriber
        NewsletterSubscriber.objects.create(email=email)

        # Send confirmation email via Brevo SDK (same pattern as contact form)
        try:
            confirmation_html = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto; padding: 20px;">
    <div style="text-align: center; padding: 20px 0; background-color: #f8a800;">
        <img src="https://fcss-web.onrender.com/static/images/icon/school__logo-removebg-preview.png"
             alt="School Logo" style="height: 60px; margin-bottom: 8px;"><br>
        <h2 style="color: white; margin: 0;">Fatima Convent Senior Secondary School</h2>
        <p style="color: white; margin: 5px 0;">Fatima Nagar, Bongaon, Rangia, Assam</p>
    </div>
    <div style="padding: 30px; background-color: #fff; border: 1px solid #eee;">
        <h3>You're subscribed! 🎉</h3>
        <p>Thank you for subscribing to the Fatima Convent School newsletter.</p>
        <p>You'll receive updates about upcoming events, news, and announcements from our school.</p>
        <p style="color: #999; font-size: 12px;">If you did not subscribe, please ignore this email.</p>
    </div>
    <div style="text-align: center; padding: 15px; background-color: #333; color: white; font-size: 12px;">
        <p style="margin: 0;">Fatima Convent Senior Secondary School</p>
        <p style="margin: 5px 0;">📞 +91 9954950683 | ✉️ fatimaschoolrangia@gmail.com</p>
    </div>
</body>
</html>
"""
            # Use Brevo SDK directly — Django's SMTP backend can silently fail on Render
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.BREVO_API_KEY
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(configuration)
            )
            confirm_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": email}],
                sender={"email": settings.DEFAULT_FROM_EMAIL},
                subject='Newsletter Subscription Confirmed — Fatima Convent School',
                html_content=confirmation_html,
            )
            api_instance.send_transac_email(confirm_email)
            print("NEWSLETTER CONFIRMATION EMAIL SENT SUCCESSFULLY")
        except ApiException as e:
            # Log but don't block the success response — subscriber is already saved
            print(f"NEWSLETTER EMAIL ERROR (Brevo): {str(e)}")
        except Exception as e:
            print(f"NEWSLETTER EMAIL ERROR: {str(e)}")

        return JsonResponse({
            'status': 'success',
            'message': 'Thank you for subscribing!'
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})



def fee_structure(request):
    fees = FeeStructure.objects.filter(is_active=True)
    return render(request, 'fee_structure.html', {'fees': fees})



# Student Portal code
def _send_otp_email(email, otp_code):
    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        html = f"""
<html><body style="font-family: Arial, sans-serif; padding:20px;">
<h2>Your verification code</h2>
<p>Use this code to verify your email for Fatima Convent School admission:</p>
<h1 style="color:#f8a800;">{otp_code}</h1>
<p>This code expires in 10 minutes.</p>
</body></html>
"""
        msg = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            sender={"email": settings.DEFAULT_FROM_EMAIL},
            subject='Your OTP — Fatima Convent School Admission',
            html_content=html,
        )
        api_instance.send_transac_email(msg)
        return True
    except Exception as e:
        print(f"OTP EMAIL ERROR: {str(e)}")
        return False




def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            request.session['pending_registration'] = {
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'father_name': data['father_name'],
                'mother_name': data['mother_name'],
                'email': data['email'],
                'phone_number': data['phone_number'],
                'date_of_birth': data['date_of_birth'].isoformat(),
                'gender': data['gender'],
                'applying_class': data['applying_class'],
                'course': data.get('course', ''),
                'password_choice': data['password_choice'],
                'custom_password': data.get('custom_password', ''),
            }

            # Only email OTP
            email_otp = OTPVerification.objects.create(
                identifier=data['email'], purpose='email'
            )
            _send_otp_email(data['email'], email_otp.otp_code)

            return render(request, 'student/verify_otp.html', {
                'email': data['email'],
            })
        else:
            return render(request, 'student/register.html', {'form': form})

    form = StudentRegistrationForm()
    return render(request, 'student/register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        email_otp_input = request.POST.get('email_otp', '').strip()

        pending = request.session.get('pending_registration')
        if not pending:
            return JsonResponse({'status': 'error', 'message': 'Session expired. Please register again.'})

        email = pending['email']

        try:
            email_otp = OTPVerification.objects.filter(
                identifier=email, purpose='email', is_verified=False
            ).latest('created_at')
        except OTPVerification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'OTP not found. Please request again.'})

        if email_otp.is_expired():
            return JsonResponse({'status': 'error', 'message': 'OTP expired. Please register again.'})

        email_otp.attempts += 1
        email_otp.save()

        if email_otp.attempts > 5:
            return JsonResponse({'status': 'error', 'message': 'Too many attempts. Please register again.'})

        if email_otp.otp_code != email_otp_input:
            return JsonResponse({'status': 'error', 'message': 'Incorrect OTP.'})

        email_otp.is_verified = True
        email_otp.save()

       
      
        #   phone_verified=False,
    if request.method == 'POST':
        email_otp_input = request.POST.get('email_otp', '').strip()
        phone_otp_input = request.POST.get('phone_otp', '').strip()

        pending = request.session.get('pending_registration')
        if not pending:
            return JsonResponse({'status': 'error', 'message': 'Session expired. Please register again.'})

        email = pending['email']
        phone = pending['phone_number']

        try:
            email_otp = OTPVerification.objects.filter(
                identifier=email, purpose='email', is_verified=False
            ).latest('created_at')
            phone_otp = OTPVerification.objects.filter(
                identifier=phone, purpose='phone', is_verified=False
            ).latest('created_at')
        except OTPVerification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'OTP not found. Please request again.'})

        if email_otp.is_expired() or phone_otp.is_expired():
            return JsonResponse({'status': 'error', 'message': 'OTP expired. Please register again.'})

        email_otp.attempts += 1
        phone_otp.attempts += 1
        email_otp.save()
        phone_otp.save()

        if email_otp.attempts > 5 or phone_otp.attempts > 5:
            return JsonResponse({'status': 'error', 'message': 'Too many attempts. Please register again.'})

        if email_otp.otp_code != email_otp_input:
            return JsonResponse({'status': 'error', 'message': 'Incorrect email OTP.'})
        if phone_otp.otp_code != phone_otp_input:
            return JsonResponse({'status': 'error', 'message': 'Incorrect phone OTP.'})

        email_otp.is_verified = True
        phone_otp.is_verified = True
        email_otp.save()
        phone_otp.save()

        # Both verified — create account + application now
        if pending['password_choice'] == 'custom':
            raw_password = pending['custom_password']
        else:
            raw_password = generate_random_password()

        user = User.objects.create_user(
            username=pending['email'],
            email=pending['email'],
            password=raw_password,
            first_name=pending['first_name'],
            last_name=pending['last_name'],
        )

        # Match fee structure for class + course
        fee = FeeStructure.objects.filter(
            class_name=pending['applying_class'],
            course=pending['course'],
            is_active=True,
        ).first()

        application = StudentApplication.objects.create(
            user=user,
            first_name=pending['first_name'],
            last_name=pending['last_name'],
            father_name=pending['father_name'],
            mother_name=pending['mother_name'],
            email=pending['email'],
            phone_number=pending['phone_number'],
            date_of_birth=pending['date_of_birth'],
            gender=pending['gender'],
            applying_class=pending['applying_class'],
            course=pending['course'],
            fee_structure=fee,
            email_verified=True,
            phone_verified=True,
            password_choice=pending['password_choice'],
            status='pending_payment',
        )

        # Email login credentials only if auto-generated
        if pending['password_choice'] == 'auto':
            try:
                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key['api-key'] = settings.BREVO_API_KEY
                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                    sib_api_v3_sdk.ApiClient(configuration)
                )
                html = f"""
<html><body style="font-family: Arial, sans-serif; padding:20px;">
<h2>Your student account is ready</h2>
<p>Login email: <strong>{pending['email']}</strong></p>
<p>Temporary password: <strong>{raw_password}</strong></p>
<p>Please log in and complete your fee payment to confirm admission.</p>
</body></html>
"""
                msg = sib_api_v3_sdk.SendSmtpEmail(
                    to=[{"email": pending['email']}],
                    sender={"email": settings.DEFAULT_FROM_EMAIL},
                    subject='Your Student Account — Fatima Convent School',
                    html_content=html,
                )
                api_instance.send_transac_email(msg)
            except Exception as e:
                print(f"CREDENTIALS EMAIL ERROR: {str(e)}")

        django_login(request, user)
        del request.session['pending_registration']

        return JsonResponse({'status': 'success', 'redirect': '/student/payment/'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})