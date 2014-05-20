import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'myeujuxyyt5=qfbza@nnq-eb205gv9o)2!erqxjz3gnxtq@c1x'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fahrplan',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'yaf.urls'

WSGI_APPLICATION = 'yaf.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yaf',
        'USER': 'root',
        'PASSWORD': 'pansen',
        'HOST': '',
        'PORT': ''
    }
}

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'CET'

USE_I18N = False

USE_L10N = False

USE_TZ = True


STATIC_URL = '/static/'
