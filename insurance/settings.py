import os
import sys
# from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# A little hack to put apps into the app dir
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_PATH, "apps"))

# Usual Django settings

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'admin@directif.ru'

TIME_ZONE = "Europe/Moscow"
LANGUAGE_CODE = 'RU-ru'
USE_I18N = True
USE_L10N = True

# ========== Static/media files urls/paths ==========
MEDIA_ROOT = os.path.join(PROJECT_PATH, '../media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_PATH, '../static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# ========== Usual Django settings ==========

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'insurance.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
    os.path.join(PROJECT_PATH, 'apps','calc','templates'),
    os.path.join(PROJECT_PATH, 'apps','notification','templates'),
    os.path.join(PROJECT_PATH, 'apps','ins_notification','templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'ins_notification.context_processors.questions',
    'notification.context_processors.notification',
    'email_login.context_processors.context_regform',
)

INSTALLED_APPS = (
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',

    # Third-party apps
    'registration',
    'django_ipgeobase',
    'django_messages',
    'notification',
    'captcha',

    # Projects apps
    'profile', # user profile file and private cabinet
    'calc',     # insurance policy related fields
    'ins_flatpages',                 # Reconfiguration of 'django.contrib.flatpages'
    'ins_notification',               # Notifications system for this site
    'news'
    )

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
    os.path.join(PROJECT_PATH, 'apps','notification','fixtures'),
)

# Import deploy-specific settings, if present
try:
    from local_settings import *
except ImportError, e:
    pass



# ========== Custom third-party application settings ==========

# --- Login and registration ---

# Days given to a user to approve the registration, used by the registration app
ACCOUNT_ACTIVATION_DAYS = 7

# Login redirect url (should be user cabinet, but for now site root url will do)
LOGIN_REDIRECT_URL = '/profile/'

# Email login backend
AUTHENTICATION_BACKENDS = (
    'email_login.backends.AuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
REGISTRATION_BACKEND = 'email_login.backends.RegistrationBackend'

# Custom user profile chosen
AUTH_PROFILE_MODULE = "profile.UserProfile"
