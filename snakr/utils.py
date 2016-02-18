import hashlib
import random
import urllib
from urlparse import urlparse

#from django.contrib.gis.utils import GeoIP
from django.core.validators import URLValidator

import web.settings as settings

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
            dummy = _URL_VALIDATOR(myurl)
        except:
            rtn = False
            pass
        return rtn

    @staticmethod
    def initurlparts():
        return urlparse('http://www.dummyurl.com')  # this is a django 1.5.11 bug workaround

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_client_geolocation(client_ip):
        #g = GeoIP()
        #lat,lng = g.lat_lon(client_ip)
        lat = 0
        lng = 0
        return lat, lng
