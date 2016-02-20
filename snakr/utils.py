import hashlib
import random
import urllib
from urlparse import urlparse
import secure.settings as settings
from django.core.validators import URLValidator

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
    def get_demographics(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        # if request.method == 'GET':
        #     slatlong = request.GET.get('X-AppEngine-CityLatLong')
        #     lat = slatlong.split(',')[0]
        #     lng = slatlong.split(',')[1]
        #     city = request.GET.get('X-AppEngine-City')
        #     country = request.GET.get('X-AppEngine-Country')
        # elif request.method == 'POST':
        #     slatlong = request.META.get('X-AppEngine-CityLatLong')
        #     lat = slatlong.split(',')[0]
        #     lng = slatlong.split(',')[1]
        #     city = request.META.get('X-AppEngine-City')
        #     country = request.META.get('X-AppEngine-Country')
        # else:
        lat = 0
        lng = 0
        city = 'unknown'
        country = 'unknown'
        return ip, lat, lng, city, country

    @staticmethod
    def is_validnsp(normalized_shorturl_path):
        rtn = False
        if normalized_shorturl_path.startswith("/"):
            rtn = True
            for c in normalized_shorturl_path[1:]:
                if settings.SHORTURL_PATH_ALPHABET.find(c) == -1:
                    rtn = False
                    break
        return rtn


