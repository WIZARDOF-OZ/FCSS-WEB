from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
from App.models import Banner, About, GalleryItem
def home(request):
    banner_images = list(Banner.objects.all())
    return render(request, 'index.html', {'banner_images': banner_images})

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

        name     = request.POST.get('name', '').strip()
        surname  = request.POST.get('surname', '').strip()
        email    = request.POST.get('email', '').strip()
        need     = request.POST.get('need', '').strip()
        message  = request.POST.get('message', '').strip()

        # Duplicate submission guard using cache
        # Creates a unique key from the form data
        import hashlib
        submission_key = hashlib.md5(
            f"{name}{surname}{email}{need}{message}".encode()
        ).hexdigest()
        cache_key = f"contact_form_{submission_key}"

        if cache.get(cache_key):
            # Same form was already submitted recently, silently succeed
            return render(request, 'contact.html', {'success': True})

        # Store in cache for 30 seconds to block duplicates
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
            cache.delete(cache_key)  # clear so they can resubmit after fixing
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

        try:
            from django.core.mail import EmailMessage as DjangoEmailMessage
            mail = DjangoEmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.EMAIL_HOST_USER],
                reply_to=[email],
            )
            mail.send(fail_silently=False)
               # Confirmation email to the person who submitted
            confirmation_html = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto; padding: 20px;">
    
    <div style="text-align: center; padding: 20px 0; background-color: #f8a800;">
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

            confirmation = DjangoEmailMessage(
    subject='We received your message — Fatima Convent School',
    body=confirmation_html,
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=[email],
)
            confirmation.content_subtype = 'html'  # this tells Django to send as HTML
            confirmation.send(fail_silently=True)
            return render(request, 'contact.html', {'success': True})

        except Exception as e:
            cache.delete(cache_key)  # clear so they can retry
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
        'gallery': gallery_images
    })