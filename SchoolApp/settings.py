from pathlib import Path
import os
import environ
from django.templatetags.static import static
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
SCHOOL_EMAIL = os.environ.get('SCHOOL_EMAIL')
BREVO_API_KEY = os.environ.get('BREVO_API_KEY')

SECRET_KEY = env('SECRET_KEY', default='test-key')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
# RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')

INSTALLED_APPS = [
    'unfold',   
    "unfold.contrib.filters",
    "unfold.contrib.forms",                  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',          
    'cloudinary',
    'App',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SchoolApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SchoolApp.wsgi.application'
CSRF_TRUSTED_ORIGINS = ['https://fcss-web.onrender.com']

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3')
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

CONN_MAX_AGE = 60  # reuse DB connections instead of reconnecting each request

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage' 

# Storage -> Static/Media
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Test -> Cloudinary

import cloudinary
cloudinary.config(
    cloud_name=env('CLOUDINARY_CLOUD_NAME'),
    api_key=env('CLOUDINARY_API_KEY'),
    api_secret=env('CLOUDINARY_API_SECRET'),
)

###################

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


EMAIL_TIMEOUT = 10
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')


# Unfold Customization

UNFOLD = {
    "STYLES": [],
    "SCRIPTS": [],
    "SITE_TITLE": "FCSS Admin",
    "SITE_HEADER": "FCSS Administration",
    "SITE_URL": "/",
    "SITE_LOGO": lambda request: static("images/icon/school__logo-removebg-preview.png"),
    "SITE_LOGO_COLLAPSED": lambda request: static("images/icon/school__logo-removebg-preview.png"),
    "SITE_FAVICON": lambda request: static("images/icon/favicon.ico"),  # add this
    "LOGIN": {
        "title": "FCSS Administration",
        "description": "Welcome to Fatima Convent Senior Secondary School Admin Panel",
    },
    "SIDEBAR": {
        "show_search": True,   # search bar in sidebar
        "show_all_applications": True,
    },
    "COLORS": {
        "primary": {
            "50": "255 251 235",
            "100": "254 243 199",
            "200": "253 230 138",
            "300": "252 211 77",
            "400": "251 191 36",
            "500": "245 158 11",
            "600": "217 119 6",
            "700": "180 83 9",
            "800": "146 64 14",
            "900": "120 53 15",
            "950": "69 26 3",
        },
    },
}

# Security settings for production

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True