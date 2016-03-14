
import os
import string
from snakr.gae import gaeinit
gaeinit()
import snakr.ipaddr # must be AFTER gaeinit()

GAE_APP_NAME = 'your-GAE-app-name-here'
GAE_PROJECT_ID = 'your-GAE-project-id'
GAE_HOST = GAE_PROJECT_ID + '.appspot.com'
GCS_INSTANCE_NAME = 'your-GCS-instance-name'

SNAKR_VERSION = '1.0.2'

ADMINS = ()
MANAGERS = ADMINS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY  = '???????????????????????????????????????????????????'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    GAE_APP_NAME,
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'web.urls'

import os.path
temp_path = os.path.realpath('.')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [temp_path +"/templates"],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'django.core.context_processors.static',
            ],
            'loaders': [
              'django.template.loaders.filesystem.Loader',
              'django.template.loaders.app_directories.Loader',
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
__SNAKR__VERSION__ = '1.0.1'

ADMINS = ()
MANAGERS = ADMINS

LOG_PATH = '{}/logs'.format(BASE_DIR)
IGNORED_PATHS = ['/admin', '/static', '/logs']
RESPONSE_FIELDS = ('status', 'reason', 'charset', 'headers', 'content')

# host (netloc) of the short URL to use
SHORTURL_HOST = "your.short.com"
SECURE_SHORTURL_HOST = GAE_HOST

ALLOWED_HOSTS = [
    GAE_HOST,
    SHORTURL_HOST,
    u'127.0.0.1',
    u'localhost'
]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

SNAKRDB_DEBUG_DB = "DEBUG"

import os
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):

    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/your-GAE-project-id:your-GCS-instance-name',
            'NAME': 'your-GCS-database-name',
            'USER': 'root',    # sounds crazy, but "root" is required by GAE for production connection (hmmmmmmmmmm)
        }
    }

elif SNAKRDB_DEBUG_DB == "DEBUG":

    gcsIP = 'your-IPv6-GCS-addess'
    try:
        mypublicIP = snakr.ipaddr.PublicIP.get()
        if mypublicIP.version == 4:
            gcsIP = 'your-IPv4-GCS-address'
    except:
        pass

    # host (netloc) of the short URL to use
    SHORTURL_HOST = "localhost:8080"
    SECURE_SHORTURL_HOST = SHORTURL_HOST

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': gcsIP,
            'NAME': 'your-GCS-database-name',
            'USER': 'your-GCS-remote-QA-user-name-do-not-use-root-for-this',
            'PASSWORD': 'your-GCS-remote-QA-user-password',
            'OPTIONS':  {
                        'ssl': {'ca':   '/path-to-your-local-server-ca.pem',
                                'cert': '/path-to-your-local-client-cert.pem',
                                'key':  '/path-to-your-local-client-key.pem'
                                }
                          },
        }
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your-GCS-database-name',
            'USER': 'your-GCS-local-user-name',
            'PASSWORD': 'your-GCS-local-user-password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

# [END db_setup]

# Max retries on hash collision detection
MAX_RETRIES = 3

# Number of alphabetic characters in the short URL path (min 6, max 12)
SHORTURL_PATH_SIZE = 6

# Character set to use for the short URL path. Remove easily-confused characters "0", "O", "o", "1", and "l". Keep "L".
SHORTURL_PATH_ALPHABET = string.digits + string.letters
SHORTURL_PATH_ALPHABET = SHORTURL_PATH_ALPHABET.replace("0","").replace("O","").replace("o","").replace("1","").replace("l","")

# DON"T change this
APPEND_SLASH=False

# If the SHORTURL_HOST or SECURE_SHORTURL_HOST value is entered into a browser with no path, it will redirect to this page
INDEX_HTML="your-desired-static-index-html-page"

# If True, enable capture of the target long url's OpenGraph title ("og:title") and return it in the JSON along with the short url
# See: http://ogp.me
# For the Python PyOpenGraph site: https://pypi.python.org/pypi/PyOpenGraph
OGTITLE = True

RETURN_ALL_META = DEBUG

#
# Logging messages
#
# Enable/disable HTTP 302, 400, 404 error logging
ENABLE_LOGGING = True
VERBOSE_LOGGING = False
DATABASE_LOGGING = True
LOG_HTTP200 = True
LOG_HTTP302 = True
LOG_HTTP400 = True
LOG_HTTP403 = True
LOG_HTTP404 = True

# sorted in rough order of probability of occurrence for lookup performance
CANONICAL_MESSAGES = {
        'ROBOT'                         : '403 Permission Denied',
        'HTTP_302'                      : '302 Redirecting to {%s}',
        'HTTP_404'                      : 'ERROR, URL {%s} not found (404)',
        'LONG_URL_SUBMITTED'            : '200 Long URL {%s} submitted',
        'VANITY_PATH_EXISTS'            : 'ERROR, the proposed vanity path for the new short URL is already in use.',
        'SHORT_URL_ENCODING_MISMATCH'   : 'ERROR, the short URL sent to this service is encoded differently from the original short URL provided and may pose a security risk. DO NOT USE the altered version.',
        'SHORT_URL_NOT_FOUND'           : 'ERROR, URL {%s} is not recognized by this service.',
        'SHORT_URL_MISMATCH'            : 'ERROR, the short URL sent to this service is different from the original short URL provided and may pose a security risk. DO NOT USE the altered version.',
        'LONG_URL_MISSING'              : 'ERROR, no long URL was submitted to the service.',
        'LONG_URL_INVALID'              : 'ERROR, the URL {%s} submitted for shortening is invalid.',
        'LONG_URL_RESUBMITTED'          : '200, Long URL {%s} resubmitted',
        'MALFORMED_REQUEST'             : 'ERROR, I don''t understand this request.',
        'STARTUP'                       : 'Snakr starting',
        'PYTHON_VERSION'                : 'Python version %s',
        'DJANGO_VERSION'                : 'Django version %s',
        'SHUTDOWN'                      : 'Snakr stopping',
        'ILLEGAL MAX_RETRIES'           : 'ERROR, MAX_RETRIES must be between 1 and 3, but is actually set to %d' % MAX_RETRIES,
        'EXCEEDED_MAX_RETRIES'          : 'ERROR, exceeded %d tries to generate new short URL.' % MAX_RETRIES,
        'HASH_COLLISION'                : 'WARNING, hash collision detected on URL {%s}.',
    }

MESSAGE_OF_LAST_RESORT = 'ERROR, an unknown exception occurred'

