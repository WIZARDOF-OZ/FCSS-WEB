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
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
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