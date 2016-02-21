import hashlib
import random
import urllib
from urlparse import urlparse
import secure.settings as settings
from django.core.validators import URLValidator
from django.core.exceptions import SuspiciousOperation

_URL_VALIDATOR = URLValidator()

class utils:


    @staticmethod
    def get_encodedurl(myurl):
        """Returns an encoded version of the passed URL."""
        return urllib.quote(myurl).encode('utf8')


    @staticmethod
    def get_decodedurl(myurl):
        """Returns an decoded version of the passed URL."""
        return urllib.unquote(myurl.decode('utf8'))


    @staticmethod
    def get_longurlhash(myurl):
        """Returns a SHA1 hash of the quoted version of the passed URL."""
        # it has to fit into a bigint on MySQL (max = 18446744073709551615), hence the 98-bit-shift
        x = long(hashlib.sha1(urllib.quote(myurl).encode('utf8')).hexdigest(),16) >> 98
        return x


    @staticmethod
    def get_shorturlhash(myurl):
        """Returns a SHA1 hash of the UNquoted version of the passed URL."""
        # it has to fit into a bigint on MySQL (max = 18446744073709551615), hence the 98-bit-shift
        x = long(hashlib.sha1(urllib.unquote(myurl).encode('utf8')).hexdigest(),16) >> 98
        return x


    @staticmethod
    def get_hash(str):
        """Returns a SHA1 hash of the passed string as-encoded"""
        # it has to fit into a bigint on MySQL (max = 18446744073709551615), hence the 98-bit-shift
        x = long(hashlib.sha1(str).hexdigest(),16) >> 98
        return x


    @staticmethod
    def get_shorturlcandidate():
        return ''.join(random.SystemRandom().choice(settings.SHORTURL_PATH_ALPHABET) for _ in range(
            settings.SHORTURL_PATH_SIZE))


    @staticmethod
    def is_url_valid(myurl):
        rtn = True
        try:
            dummy = _URL_VALIDATOR(utils.get_decodedurl(myurl))
        except:
            rtn = False
            pass
        return rtn


    @staticmethod
    def initurlparts():
        return urlparse('http://www.dummyurl.com')  # this is a django 1.5.11 bug workaround


    @staticmethod
    def get_clientinfo(request):
        # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip = x_forwarded_for.split(',')[0]
        # else:
        #     ip = request.META.get('REMOTE_ADDR')
        # slatlong = request.META.get('X-AppEngine-CityLatLong')
        # raise SuspiciousOperation("<%s>" % slatlong)
        # if slatlong:
        #     lat = slatlong.split(',')[0]
        #     lng = slatlong.split(',')[1]
        # else:
        #     lat = 0.0
        #     lng = 0.0
        # city = request.META.get('X-AppEngine-City')
        # if not city:
        #     city="unknown"
        # country = request.META.get('X-AppEngine-Country')
        # if not country:
        #     country="unknown"
        # http_host = request.META.get('HTTP_HOST')
        # if not http_host:
        #     http_host="unknown"
        # http_referrer = request.META.get('HTTP_REFERRER')
        # if not http_referrer:
        #     http_referrer="unknown"
        # user_agent = request.META.get('USER_AGENT')
        # if not user_agent:
        #     user_agent="unknown"
        # return ip, lat, lng, city, country, http_host, http_referrer, user_agent
        return 'unknown',0.0,0.0,'unknown','unknown','unknown','unknown','unknown'


    @staticmethod
    def is_validnsp(normalized_shorturl_path):
        rtn = False
        if normalized_shorturl_path.startswith('/'):
            rtn = True
            for c in normalized_shorturl_path[1:]:
                if settings.SHORTURL_PATH_ALPHABET.find(c) == -1:
                    rtn = False
                    break
        return rtn
