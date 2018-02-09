"""
Django settings for mrs project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import shutil
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'notsecret')

DEBUG = os.getenv('DEBUG', False)

if not DEBUG and 'SECRET_KEY' not in os.environ:
    raise Exception('$SECRET_KEY is required if DEBUG is False')

if 'ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')]

if not DEBUG and 'ALLOWED_HOSTS' not in os.environ:
    raise Exception('$ALLOWED_HOSTS is required if DEBUG is False')

LOGIN_REDIRECT_URL = '/mrsrequest/'

# Application definition

INSTALLED_APPS = [
    'contact',
    'institution',
    'person',
    'mrs',
    'mrsrequest',
    'mrsattachment',

    'jfu',
    'material',
    'webpack_loader' if shutil.which('npm') else 'webpack_mock',
    'django_humanize',

    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'mrs.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "contact.context_processors.contact_form",
                "mrs.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = 'mrs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.getenv('DB_USER', None),
        'PASSWORD': os.getenv('DB_PASSWORD', None),
        'HOST': os.getenv('DB_HOST', None),
        'PORT': os.getenv('DB_PORT', None),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.{}'.format(n),
    } for n in [
        'UserAttributeSimilarityValidator',
        'MinimumLengthValidator',
        'CommonPasswordValidator',
        'NumericPasswordValidator',
    ]
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/


LOCALE = 'fr_FR'
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = os.environ.get('TIME_ZONE', 'Europe/Paris')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', os.path.join(BASE_DIR, 'collected'))
STATICFILES_DIRS = [os.path.join(os.path.dirname(__file__), 'static')]

DEFAULT_FILE_STORAGE = 'db_file_storage.storage.DatabaseFileStorage'

EMAIL_HOST = os.getenv('EMAIL_HOST', None)
EMAIL_PORT = os.getenv('EMAIL_PORT', None)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', None)
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', None)
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'from@example.com')
TEAM_EMAIL = os.getenv('TEAM_EMAIL', 'team@example.com')
LIQUIDATION_EMAIL = os.getenv('LIQUIDATION_EMAIL', 'liquidation@example.com')

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', EMAIL_BACKEND)

try:
    import raven  # noqa
except ImportError:
    raven = None
else:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

RAVEN_CONFIG = dict()
if os.getenv('SENTRY_DSN'):
    RAVEN_CONFIG['dsn'] = os.getenv('SENTRY_DSN')
if os.getenv('INSTANCE'):
    RAVEN_CONFIG['environment'] = os.getenv('INSTANCE')
if os.getenv('GIT_COMMIT'):
    RAVEN_CONFIG['release'] = os.getenv('GIT_COMMIT')
elif raven:
    repo = os.path.join(os.path.dirname(__file__), '..', '..')
    if os.path.exists(os.path.join(repo, '.git')):
        RAVEN_CONFIG['release'] = raven.fetch_git_sha(repo)

if os.getenv('LOG'):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'file.error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': os.path.join(
                    os.getenv('LOG'),
                    'django.error.log',
                ),
                'formatter': 'simple',
            },
            'file.info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(
                    os.getenv('LOG'),
                    'django.info.log',
                ),
                'formatter': 'simple'
            },
            'file.debug': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(
                    os.getenv('LOG'),
                    'django.debug.log',
                ),
                'formatter': 'simple'
            },
        },
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(name)s %(message)s'
            },
        },
        'loggers': {
            'django': {
                'handlers': [
                    'file.error',
                    'file.info',
                    'file.debug',
                    'console'
                ],
                'level': 'DEBUG' if DEBUG else 'INFO',
                'propagate': True,
            },
        },
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'loggers': {
            '*': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }

if DEBUG:
    try:
        import dbdiff  # noqa
    except ImportError:
        pass
    else:
        INSTALLED_APPS += ('dbdiff',)

    try:
        import debug_toolbar  # noqa
    except ImportError:
        pass
    else:
        INSTALLED_APPS += ('debug_toolbar',)
        MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
        INTERNAL_IPS = ['172.17.0.1', '127.0.0.1']
