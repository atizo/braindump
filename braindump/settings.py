import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET', '%g#i3#6@*6v%81z)xsx6a*4zb3k^%3!b5*aof38^w7f8c6l6=q')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not bool(os.environ.get('DJANGO_NO_DEBUG', ''))

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'rest_framework',
    'easy_thumbnails',
    'easy_thumbnails.optimize',
    'storages',
    'south',
    'django_nose',
    'brainstorming',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'braindump.urls'

WSGI_APPLICATION = 'braindump.wsgi.application'


# Parse database configuration from $DATABASE_URL
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='postgres://braindump:test@localhost/braindump')
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Zurich'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static asset configuration
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'preview': {'size': (640, 400), 'crop': True},
        'large': {'size': (1920, 1920), 'crop': 'scale'},
    },
}

THUMBNAIL_CACHE_DIMENSIONS = True

THUMBNAIL_OPTIMIZE_COMMAND = {
    'png': '/usr/bin/optipng {filename}',
    'gif': '/usr/bin/optipng {filename}',
    'jpeg': '/usr/bin/jpegoptim {filename}'
}


if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, '../client/app/static'),
    )

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, '../client/app'),
    )
else:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'templates'),
    )

# Mail settings
FORM_MAIL = 'braindump@heroku.com'
if 'SENDGRID_USERNAME' in os.environ:
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

if not DEBUG:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_FILE_OVERWRITE = False

    CACHES = {
        'default': {
            'BACKEND': 'django_bmemcached.memcached.BMemcached',
            'LOCATION': os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
            'OPTIONS': {
                'username': os.environ.get('MEMCACHEDCLOUD_USERNAME'),
                'password': os.environ.get('MEMCACHEDCLOUD_PASSWORD')
            }
        }
    }

SITE_ID = 1