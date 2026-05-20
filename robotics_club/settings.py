"""
Django settings for robotics_club project.
Production-ready: Render + Neon + Cloudinary + Email (Brevo)
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env locally
env_path = BASE_DIR / '.env.local'
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-change-me-in-production'
)

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com"
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'anymail',

    # Local apps
    'accounts',
    'core',
    'events',
    'teams',
]

# =========================================================
# MIDDLEWARE
# =========================================================

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

ROOT_URLCONF = 'robotics_club.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'robotics_club.wsgi.application'

# =========================================================
# DATABASE (NEON / RAILWAY fallback)
# =========================================================

DATABASE_URL = os.environ.get('DATABASE_URL', '')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =========================================================
# AUTH
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================================================
# MEDIA (CLOUDINARY PRODUCTION)
# =========================================================

# 1. Keep Cloudinary apps stable in your main INSTALLED_APPS list above:
# INSTALLED_APPS = [ ..., 'cloudinary_storage', 'cloudinary', 'accounts', ... ]
# Note: 'cloudinary_storage' MUST be placed BEFORE 'django.contrib.staticfiles' 
# if managing static files, or simply keep it near the top of third-party apps.

# 2. Refactor the Media Storage block to be explicitly declarative:
# =========================================================
# MEDIA (CLOUDINARY PRODUCTION / LOCAL FALLBACK)
# =========================================================

CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')

if CLOUDINARY_CLOUD_NAME:
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }

    # Points Cloudinary to look inside your asset folder structure 
    MEDIA_URL = "/media/"
else:
    # Standard configuration for local offline development
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True
USE_TZ = True

# =========================================================
# EMAIL (BREVO / ANYMAIL)
# =========================================================

ADMIN_EMAIL = "rbtkec@gmail.com"

if os.environ.get('DATABASE_URL'):
    EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"

    ANYMAIL = {
        "SENDINBLUE_API_KEY": os.environ.get("BREVO_API_KEY"),
    }

    DEFAULT_FROM_EMAIL = f"Robotics Club <{ADMIN_EMAIL}>"
    SERVER_EMAIL = ADMIN_EMAIL
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = ADMIN_EMAIL

# =========================================================
# DEFAULT AUTO FIELD
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'