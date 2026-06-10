from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from App.models import Banner, About, GalleryItem
import hashlib
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def home(request):
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