import os
import string
from secure.gae import gaeinit

gaeinit()

# from djangoappengine.utils import on_production_server

# names defined here
GAE_APP_NAME = 'snakr'
GCS_INSTANCE_NAME = 'YourGCSQLdbName'
GAE_PROJECT_ID = os.environ['APPLICATION_ID']
SNAKR_VERSION = '1.0.%s' % os.environ['CURRENT_VERSION_ID']
GAE_HOST = os.environ.get('SNAKR_GAE_HOST')
GAE_QA_HOSTS = u'.%s' % GAE_HOST
ROOT_URLCONF = os.environ.get('SNAKR_ROOT_URLCONF')
PERSIST_EVENTSTREAM_TO_CLOUDSQL = True
PERSIST_EVENTSTREAM_TO_DATASTORE = False
ENABLE_BOTPROTECTION = True
ENABLE_BLACKLISTING = True
THRIDPARTY_IP_BLACKLISTS = [
         ('PAN Spamhous DROP', 'https://panwdbl.appspot.com/lists/shdrop.txt'),
         ('PAN Spamhous EDROP', 'https://panwdbl.appspot.com/lists/shedrop.txt'),
         ('PAN OpenBL Blocklist', 'https://panwdbl.appspot.com/lists/openbl.txt'),
         ('PAN BruteForceBlocker', 'https://panwdbl.appspot.com/lists/bruteforceblocker.txt'),
         ('PAN Malware Domain List', 'https://panwdbl.appspot.com/lists/mdl.txt'),
         ('PAN Emerging Threats TOR', 'https://panwdbl.appspot.com/lists/ettor.txt'),
         ('PAN Emerging Threats Known Compromised Hosts', 'https://panwdbl.appspot.com/lists/etcompromised.txt'),
         ('PAN DShield Recommended Block List', 'https://panwdbl.appspot.com/lists/dshieldbl.txt'),
         ('PAN SSL Abuse IP List', 'https://panwdbl.appspot.com/lists/sslabuseiplist.txt'),
         ('PAN Zeus Tracker Bad IPs List', 'https://panwdbl.appspot.com/lists/zeustrackerbadips.txt'),
]

# host (netloc) of the short URL to use
SHORTURL_HOST = "YourShortUrlRootGoes.here"
# 2/20/2016 secure short urls are not redirecting with bret.guru.
# Workaround until I can get an ssl certificate for bret.guru to support secure forwarding.
SECURE_SHORTURL_HOST = GAE_HOST

ALLOWED_HOSTS = [
    GAE_HOST,
    SHORTURL_HOST,
    SECURE_SHORTURL_HOST,
    GAE_QA_HOSTS,
    u'127.0.0.1',
    u'localhost',
]

ADMINS = ()
MANAGERS = ADMINS

if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    BASE_DIR = '/YourLocalRootDirHere'
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_PATH = '{}/logs'.format(BASE_DIR)
IGNORED_PATHS = ['/admin', '/static', '/logs']
RESPONSE_FIELDS = ('status', 'reason', 'charset', 'headers', 'content')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '??????????????????????????????????????????????????'

# Application definition

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
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
    #    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #    'django.middleware.security.SecurityMiddleware',
)

import os.path

temp_path = os.path.realpath('.')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [temp_path + "/templates"],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.reports.context_processors.request',
                'django.reports.context_processors.static',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

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

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATIC_ROOT = (os.path.join(SITE_ROOT, 'static/'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

SNAKRDB_DEBUG_DB = "DEBUG"

import os

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):

    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/YourGAEProjectName:YourGCSQLdbName',
            'NAME': 'YourGAEProjectName',
            'USER': 'root',  # sounds crazy, but "root" is required by GAE for production connection (hmmmmmmmmmm)
        },
    }

    DATASTORE_ENTITY = 'EventStream'

elif SNAKRDB_DEBUG_DB == "DEBUG":

    gcsIP = 'YourGCSQLIPv6Here'
    import snakr.ipaddr as ip  # leave this import here

    try:
        mypublicIP = ip.PublicIP.get()
        if mypublicIP.version == 4:
            gcsIP = 'YourGCSQLIPv4HereIfYouHaveOne'
    except:
        pass

    # host (netloc) of the short URL to use
    SHORTURL_HOST = "localhost:8080"
    # 2/20/2016 secure short urls are not redirecting with bret.guru.
    # Workaround until I can get an ssl certificate for bret.guru to support secure forwarding.
    SECURE_SHORTURL_HOST = SHORTURL_HOST

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': gcsIP,
            'NAME': 'YourGAEProjectName',
            'USER': 'YourGCSQLdbNameo',
            'PASSWORD': 'YourGCSQLdbPassword',
            'OPTIONS': {
                'ssl': {
                    'ca': '/YourCertLocation/server-ca.pem',
                    'cert': '/YourCertLocation/client-cert.pem',
                    'key': '/YourCertLocation/client-key.pem'
                    }
            }
        },
    }

    DATASTORE_ENTITY = 'EventStream'

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'YourGAEProjectName',
            'USER': 'dbo',
            'PASSWORD': 'YourGAEProjectNamedbo',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        },
    }

    DATASTORE_ENTITY = None

# [END db_setup]

# Max retries on hash collision detection
MAX_RETRIES = 3

# Number of alphabetic characters in the short URL path (min 6, max 12)
SHORTURL_PATH_SIZE = 6

# Character set to use for the short URL path. Remove easily-confused characters "0", "O", "o", "1", and "l". Keep "L".
SHORTURL_PATH_ALPHABET = string.digits + string.letters
SHORTURL_PATH_ALPHABET = SHORTURL_PATH_ALPHABET.replace("0", "").replace("O", "").replace("o", "").replace("1",
                                                                                                           "").replace(
    "l", "")

# DON"T change this
APPEND_SLASH = False

# If the SHORTURL_HOST or SECURE_SHORTURL_HOST value is entered into a browser with no path, it will redirect to this
#  page
INDEX_HTML = "http://www.linkedin.com/in/YourLinkedInProfilePageWorksGreatHere"

# If True, enable capture of the target long url's OpenGraph title ("og:title") and return it in the JSON along with
# the short url
# See: http://ogp.me
# For the Python PyOpenGraph site: https://pypi.python.org/pypi/PyOpenGraph
OGTITLE = True
RETURN_ALL_META = DEBUG

#
# Logging messages
#
# Enable/disable logging features
ENABLE_LOGGING = True
VERBOSE_LOGGING = False
DATABASE_LOGGING = True
LOG_HTTP200 = True
LOG_HTTP302 = True
LOG_HTTP400 = True
LOG_HTTP403 = True
LOG_HTTP404 = True
DATASTORE_VERIFICATION = True

# sorted in rough order of probability of occurrence for lookup performance
CANONICAL_MESSAGES = {
    'ROBOT': '403 Permission Denied',
    'BLACKLIST': '403 Permission Denied',
    'HTTP_302': '302 Redirecting to %s',
    'HTTP_404': 'ERROR, URL %s not found (404)',
    'LONG_URL_SUBMITTED': '200 Long URL %s submitted',
    'VANITY_PATH_EXISTS': 'ERROR, the proposed vanity path for the new short URL is already in use.',
    'SHORT_URL_ENCODING_MISMATCH': 'ERROR, the short URL sent to this service is encoded differently from the '
                                   'original short URL provided and may pose a security risk. DO NOT USE the altered '
                                   'version.',
    'SHORT_URL_NOT_FOUND': 'ERROR, URL %s is not recognized by this service.',
    'SHORT_URL_MISMATCH': 'ERROR, the short URL sent to this service is different from the original short URL '
                          'provided and may pose a security risk. DO NOT USE the altered version.',
    'LONG_URL_MISSING': 'ERROR, no long URL was submitted to the service.',
    'LONG_URL_INVALID': 'ERROR, the URL %s submitted for shortening is not a valid URL.',
    'LONG_URL_DOESNTEXIST': 'ERROR, the URL %s submitted for shortening does not exist or was not found.',
    'LONG_URL_RESUBMITTED': '200, Long URL %s resubmitted',
    'MALFORMED_REQUEST': 'ERROR, I don''t understand this request.',
    'STARTUP': 'STARTING Snakr version %s',
    'PYTHON_VERSION': 'Python version %s',
    'DJANGO_VERSION': 'Django version %s',
    'SHUTDOWN': 'Snakr stopping',
    'ILLEGAL MAX_RETRIES': 'ERROR, MAX_RETRIES must be between 1 and 3, but is actually set to %d' % MAX_RETRIES,
    'EXCEEDED_MAX_RETRIES': 'ERROR, exceeded %d tries to generate new short URL.' % MAX_RETRIES,
    'HASH_COLLISION': 'WARNING, hash collision detected on URL %s.',
    'GOOGLEDATASTORE_UNAVAILABLE': 'ERROR, Google Datastore is not configured or is not reachable. Check your '
                                   'settings and the Google Cloud Dashboard for system status.',
    'GOOGLEDATASTORE_ERROR': 'ERROR, from Google Datastore: %s.',
}

MESSAGE_OF_LAST_RESORT = 'ERROR, an unknown exception occurred'

EVENT_TYPES = (
    ('B', '403 Bot/Blacklisted'),
    ('D', 'Debug'),
    ('E', 'Error'),
    ('I', 'Information'),
    ('L', '200 New Long URL Submitted'),
    ('R', '200 Existing Long URL Resubmitted'),
    ('S', '302 Short URL Redirect'),
    ('T', 'Test Data'),
    ('W', 'Warning'),
    ('X', 'Exception'),
    ('Z', 'Incomplete')
)

EVENT_STATUSES = (
    ('B', 1),
    ('D', -1),
    ('E', 1),
    ('I', 0),
    ('L', 0),
    ('R', 0),
    ('S', 0),
    ('T', 99),
    ('W', 1),
    ('X', 1),
    ('Z', -1)
)

WHITELISTED_BOTS = ['googlebot', 'googlecloudmonitoring', 'appengine-google', 'msnbot', 'bingbot', 'slurp', 'twitterbot', 'bot/1.0',
                    'Googlebot-Mobile','Googlebot-Image','Googlebot-News','Googlebot-Video','DuckDuckBot','Facebot','Applebot']


BLACKLISTED_BOTS = ['(simulated_by_webserver_stress_tool)', '/teoma', '1job', 'abot', 'adbeat', 'adgbot', 'adometrybot',
                    'adr)', 'adsbot-google', 'advanced email extractor', 'advanced+email+extractor', 'agentname',
                    'alertsite', 'apache-httpclient/4.1.1 (java 1.5)', 'apache-httpclient/4.1.1+(java+1.5)',
                    'apachebench', 'aport', 'appengine-google', 'applesyndication', 'appneta sequencer',
                    'appneta+sequencer', 'archive.org', 'argus', 'ask jeeves', 'ask+jeeves', 'atomic_email_hunter',
                    'atomz', 'auditbot', 'avantgo', 'aware', 'b2w', 'baiduspider', 'bingbot', 'bingpreview', 'bitlybot',
                    'bitvouseragent', 'blitzbot', 'bloglines', 'blp_bbot', 'bordermanager', 'catchpoint', 'cfschedule',
                    'changedetection', 'check_http', 'checkurl', 'chkd', 'citeseerxbot', 'clickajob', 'coast',
                    'combine', 'companydatatree', 'contype', 'cookiereports', 'cosmos', 'crawl', 'crescent',
                    'curious george', 'curious+george', 'curl', 'cutbot', 'd24y-aegis', 'daumoa', 'dialer',
                    'discoverybot', 'download ninja', 'download+ninja', 'drupal', 'dts agent', 'dts+agent',
                    'ec2linkfinder', 'echo', 'europarchive', 'everyonesocialbot', 'evrinid',
                    'ez publish link validator', 'ez+publish+link+validator', 'ezooms', 'facebookexternalhit',
                    'fairshare', 'favorg', 'fdm 3.x', 'fdm+3.x', 'feed43', 'feedburner', 'fetch', 'findlinks','firefox/1.',
                    'flamingo_searchengine', 'flamingosearch', 'flashget', 'freedom', 'frontier', 'funnelback',
                    'fupbot', 'genieo', 'getright', 'goldfire', 'golem', 'gomezagent', 'google web preview',
                    'google wireless transcoder', 'google+web+preview', 'google+wireless+transcoder',
                    'google-hoteladsverifier', 'googlebot', 'grabber', 'grub', 'harvest', 'help@dataminr.com',
                    'heritrix', 'hiscan', 'hitlist', 'holmes', 'htmlparser', 'http://bot.ims.ca', 'httpcomponents',
                    'httpunit', 'httrack', 'ia_archive', 'ibot', 'ichiro', 'ieautodiscovery', 'indy library',
                    'indy+library', 'infolink', 'innovantagebot', 'internal zero-knowledge agent',
                    'internal+zero-knowledge+agent', 'internet ninja', 'internet+ninja', 'internetseer', 'iopus',
                    'isearch', 'isense bot', 'isense+bot', 'isilo', 'jakarta', 'jobblebot', 'jobo', 'jobrapido',
                    'joedog', 'jooblebot', 'justview', 'keynote', 'khte', 'kinja', 'ktxn', 'larbin', 'libwww-perl',
                    'liferea', 'linkbot', 'linkchecker', 'linklint', 'linkscan', 'linkwalker', 'lisa', 'livelapbot',
                    'loadimpactpageanalyzer', 'lwp', 'lydia', 'magus bot', 'magus+bot', 'maxamine',
                    'mediapartners-google', 'metauri api', 'mfc_tear_sample', 'microsoft bits',
                    'microsoft scheduled cache content download service', 'microsoft url control', 'microsoft+bits',
                    'microsoft+scheduled+cache+content+download+service', 'microsoft+url+control', 'miva', 'mj12bot',
                    'mlbot', 'mna digital circonus check', 'mna+digital+circonus+check', 'moatbot', 'monster',
                    'moreoverbot', 'mozilla/4.0 (compatible; msie 6.0; windows nt 5.1;1813)',
                    'mozilla/4.0+(compatible;+msie+6.0;+windows+nt+5.1;1813)', 'mozilla/5.0 (compatible; msie 5.0)',
                    'mozilla/5.0+(compatible;+msie+5.0)', 'ms frontpage', 'ms search', 'ms+frontpage', 'ms+search',
                    'msnptc', 'nbot', 'nerdbynature', 'newsapp', 'newsnow', 'nextgensearchbot', 'ng/2.0', 'nielsen adr',
                    'nielsen+adr', 'nomad', 'npbot', 'nutch', 'nutscrape', 'obot', 'omniexplorer', 'oodlebot',
                    'orangebot-mobile', 'outbrain', 'panscient.com', 'paperlibot', 'paros', 'patric', 'phantomjs',
                    'pingdom', 'pioneer', 'pita', 'pluck', 'plumtree', 'postrank', 'powermarks', 'proximic', 'psbot',
                    'python-httplib', 'python-urllib', 'reconnoiter', 'riverglassscanner', 'rpt-http', 'rssreader',
                    'scan', 'scanalert', 'scc internet services - url check', 'scc+internet+services+-+url+check',
                    'scooter', 'scoutjet', 'search-engine-studio', 'search_comments\\at\\sensis\\dot\\com\\dot\\au',
                    'searchme.com/support/', 'seekbot', 'server density external llama',
                    'server+density+external+llama', 'servers alive url check', 'servers+alive+url+check', 'sherlock',
                    'shopwiki', 'simplepie', 'sitecon', 'siteimprove', 'sitevigil', 'sjn', 'slurp', 'smokeping',
                    'snapbot', 'snappreviewbot', 'snoopy', 'sohu', 'spider', 'spike', 'stackrambler', 'stuff', 'sucker',
                    'surveybot/', 'system center operations manager', 'system+center+operations+manager',
                    't-h-u-n-d-e-r-s-t-o-n-e', 'tagscanner', 'talktalk', 'teleport', 'templeton', 'terrawizbot',
                    'thunderstone', 'topix', 'trovit', 'tsmbot', 'tweetedtimes.com', 'tweetmemebot', 'twiceler',
                    'twisted pagegetter', 'twisted+pagegetter', 'ukonline', 'ultraseek', 'universalsearch',
                    'updatepatrol', 'urchin', 'vagabondo', 'vmcbot', 'vocusbot', 'voyager', 'w3c_validator', 'wapt',
                    'wasalive', 'watchfire webxm', 'watchfire+webxm', 'watchmouse', 'wbsearchbot', 'web downloader',
                    'web+downloader', 'webauto', 'webbot', 'webcapture', 'webcheck', 'webcopier', 'webdup',
                    'webmetrics', 'websitepulse', 'webtool', 'webtrends', 'wepbot', 'wfarc', 'wget', 'whatsup',
                    'wikiofeedbot', 'wikiwix-bot', 'worm', 'wusage/', 'www-mechanize', 'xenu', 'yacy', 'yahoo pipes',
                    'yahoo+pipes', 'yahoofeedseeker', 'yahooseeker', 'yandex', 'yioopbot', 'yottaamonitor', 'zealbot',
                    'zeus']
