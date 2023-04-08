"""
Django settings for mandalinka project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import io
import os
from pathlib import Path
from urllib.parse import urlparse

import environ
from google.cloud import secretmanager

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Get environemt variables from google secret manager based on the environment
env = environ.Env(
    DEBUG=(bool, False),
    USE_CLOUD_SQL_PROXY=(bool, False),
    SECRET_KEY=(str, None),
    APPENGINE_URL=(str, None),
)

client = secretmanager.SecretManagerServiceClient()

# Get environment variables from secret manager

environment_type = []

if os.getenv("DEVELOPMENT", None) in ("True", "true", "1", True):
    environment_type.append("development")
if os.getenv("STAGING", None) in ("True", "true", "1", True):
    environment_type.append("staging")
if os.getenv("PRODUCTION", None) in ("True", "true", "1", True):
    environment_type.append("production")
if not environment_type:
    raise Exception(
        f"Environment not set, please set either DEVELOPMENT, STAGING or PRODUCTION to True")
elif len(environment_type) > 1:
    raise Exception(
        f"Multiple environments set, please set only one of DEVELOPMENT, STAGING or PRODUCTION to True")

secret_env_name = f"projects/932434718756/secrets/django_settings_{environment_type}/versions/latest"

env.read_env(io.StringIO(client.access_secret_version(
    name=secret_env_name).payload.data.decode("UTF-8")))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY is not set")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to App Engine. This code takes the URL and converts it to both these settings formats.
APPENGINE_URL = env("APPENGINE_URL")
if APPENGINE_URL:
    # Ensure a scheme is present in the URL before it's processed.
    if not urlparse(APPENGINE_URL).scheme:
        APPENGINE_URL = f"https://{APPENGINE_URL}"

    ALLOWED_HOSTS = [urlparse(APPENGINE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [APPENGINE_URL]
    SECURE_SSL_REDIRECT = True
else:
    ALLOWED_HOSTS = ["*"]

# Database
# Use django-environ to parse the connection string
DATABASES = {"default": env.db()}

# If the flag as been set, configure to use proxy
USE_CLOUD_SQL_PROXY = env("USE_CLOUD_SQL_PROXY")
if USE_CLOUD_SQL_PROXY:
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432
DATABASES["default"]["TEST"] = {"NAME": "test_database"}

PASSWORD_RESET_TIMEOUT = 14400

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'graphene_django',
    'corsheaders',
    'storages',
    'utils',
    'accounts',
    'management',
    'customers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mandalinka.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mandalinka.wsgi.application'


# # Use a in-memory sqlite3 database when testing in CI systems
# # TODO(glasnt) CHECK IF THIS IS REQUIRED because we're setting a val above
# if os.getenv("TRAMPOLINE_CI", None):
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#         }
#     }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# User Verification

AUTHENTICATION_BACKENDS = ('accounts.verification.EmailVerification',)


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = "staticfiles"
STATIC_URL = "static/"
STATICFILES_DIRS = []

GRAPHENE = {
    'SCHEMA': 'mandalinka.schema.schema'
}

# Media files
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

GS_PROJECT_ID = 'brave-server-365708'
GS_BUCKET_NAME = 'mandalinka'

MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Google API KEY

GOOGLE_API_KEY = 'AIzaSyCEZTFyo0Kf5YL5SWe6vmmfEMmF5QxSTbU'


# Custom user representation model

AUTH_USER_MODEL = 'accounts.User'


# EMAILING INFO

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'mandalinkatest@gmail.com'
EMAIL_HOST_USER = 'mandalinkatest@gmail.com'
EMAIL_HOST_PASSWORD = 'affaxdalowtrsyxe'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Templates for CRISPY forms

CRISPY_ALLOWED_TEMPLATE_PACKS = ("bootstrap5", "uni_form")

CRISPY_TEMPLATE_PACK = "bootstrap5"

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%d %b. %Y, %H:%M:%S",
    'DATE_FORMAT': "%d %b, %Y",
    'TIME_FORMAT': "%H:%M:%S",
}

CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]
