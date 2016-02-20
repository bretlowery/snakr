# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Django secure for web project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/secure/

For the full list of secure and their values, see
https://docs.djangoproject.com/en/1.8/ref/secure/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import string

try:
    from dev_appserver_version import DEV_APPSERVER_VERSION
except ImportError:
    DEV_APPSERVER_VERSION = 2

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development secure - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '???????????????????????????????????????????????????'


# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = [
    'your url host (netloc) here',
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'snakr',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

import os.path
temp_path = os.path.realpath('.')
TEMPLATE_DIRS = (
    temp_path +"/templates",
)

WSGI_APPLICATION = 'web.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT='static'
STATIC_URL = '/static/'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# [START db_setup]
import os
SNAKRDB_MODE = "REMOTE"
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/your app id:your GCS instance name',
            'NAME': 'your schema name',
            'USER': 'root',    # sounds crazy, but "root" is required by GAE (hmmmmmmmmmm)
        }
    }
elif SNAKRDB_MODE == "REMOTE":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'your IP address',
            'NAME': 'your schema name',
            'USER': 'your user name',    # sounds crazy, but "root" is required by GAE (hmmmmmmmmmm)
            'PASSWORD': 'your password'
        }
    }
elif SNAKRDB_MODE == "LOCAL":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your local schema name',
            'USER': 'your local user name',
            'PASSWORD': 'your local password',
            'HOST': '127.0.0.1 or similar',
            'PORT': '3306',
        }
    }
# [END db_setup]

# Max retries on hash collision detection
MAX_RETRIES = 3

# host (netloc) of the short URL to use
SHORTURL_HOST = "your GAE appid.appspot.com OR other short url host/netloc"

# Number of alphabetic characters in the short URL path (min 6, max 12)
SHORTURL_PATH_SIZE = 6

# Character set to use for the short URL path. Remove easily-confused characters "0", "O", "o", "1", and "l". Keep "L".
SHORTURL_PATH_ALPHABET = string.digits + string.letters
SHORTURL_PATH_ALPHABET = SHORTURL_PATH_ALPHABET.replace("0","").replace("O","").replace("o","").replace("1","").replace("l","")