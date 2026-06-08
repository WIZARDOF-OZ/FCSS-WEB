from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from App.models import Banner, About, GalleryItem
import requests

# Create your views here.

def home(request):
    banner_images = list(Banner.objects.all())
    return render(request, 'index.html', {'banner_images': banner_images})

def about_view(request):
    about = list(About.objects.all())
    data = {
        'about': about,
    }
    return render(request, 'about.html', data)

def error_404(request, exception=None):
    return render(request, 'error-404.html', status=404)

def contact(request):
    if request.method == 'POST':
        # Get form data
        name     = request.POST.get('name')
        surname  = request.POST.get('surname')
        email    = request.POST.get('email')
        need     = request.POST.get('need')
        message  = request.POST.get('message')

        # Verify reCAPTCHA
        recaptcha_response = request.POST.get('g-recaptcha-response')

        if not recaptcha_response:
            return render(request, 'contact.html', {
                'error': 'Please complete the reCAPTCHA.',
                'form_data': request.POST
            })

        recaptcha_verify = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response,
            }
        )
        result = recaptcha_verify.json()

        if not result.get('success'):
            return render(request, 'contact.html', {
                'error': 'reCAPTCHA verification failed. Please try again.',
                'form_data': request.POST
            })

        # All good — handle your form data here (e.g. send email, save to DB)
        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')

def gallery(request):
    distinct_categories = GalleryItem.objects.values_list('category', flat=True).distinct()
    gallery_images = list(GalleryItem.objects.all())

    data = {
        'distinct_categories': distinct_categories,
        'gallery': gallery_images
    }
    return render(request, 'gallery.html', data)