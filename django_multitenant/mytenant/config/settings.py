import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '$a3i0-t1iq-!*8hfv$1g4ej7o6c%u)yjq^qj@x+&uq72fbt+=3'

DEBUG = True

ALLOWED_HOSTS = ['*']

SHARED_APPS = [
    'tenant_schemas',  # mandatory, should always be before any django app
    'tenants',  # you must list the app where your tenant model resides in

    # everything below here is up to your project needs
    'bootstrap3',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_db_logger', # pip install django-db-logger
    'django.contrib.admin',
    'django.contrib.auth',

]

TENANT_APPS = [
    # Your tenant-specific apps
    #'django.contrib.admin',
    # 'django.contrib.auth',
    'notes',
]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

TENANT_MODEL = 'tenants.Tenant'

MIDDLEWARE = [
    'tenant_schemas.middleware.TenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.tenant_urls'
PUBLIC_SCHEMA_URLCONF = 'config.public_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        # Use the tenant_schemas specific postgresql_backend
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': 'db_tenant',
        'USER': 'admin',
        'PASSWORD': 'datatres',
        'HOST': 'localhost',
        'PORT': 5433,
    }
}

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'

LOGIN_REDIRECT_URL = 'notes:home_notes'
LOGOUT_REDIRECT_URL = 'notes:home_notes'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# importing logger settings
# ------------------------------------------------------------------------------

try:
    from .logger_settings import *
except Exception as e:
    # in case of any error, pass silently.
    pass