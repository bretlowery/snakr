import hashlib
import random
import urllib
from urlparse import urlparse
import secure.settings as settings
from django.core.validators import URLValidator
import json
import mimetypes
import urllib2

_URL_VALIDATOR = URLValidator()


class Utils:

    def __init__(self):
        return

    @staticmethod
    def get_encodedurl(myurl):
        """Returns an encoded version of the passed URL."""
        return urllib.quote(myurl).encode('utf8').replace('%3A//','://')

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
    def get_hash(value):
        """Returns a SHA1 hash of the passed string as-encoded"""
        # it has to fit into a bigint on MySQL (max = 18446744073709551615), hence the 98-bit-shift
        if str == 'unknown':
            x = 0
        else:
            x = long(hashlib.sha1(value).hexdigest(),16) >> 98
        return x

    @staticmethod
    def get_shortpathcandidate(**kwargs):
        digits_only = kwargs.pop("digits_only", False)
        if digits_only:
            import string
            return ''.join(random.SystemRandom().choice(string.digits) for _ in range(
                settings.SHORTURL_PATH_SIZE))
        else:
            return ''.join(random.SystemRandom().choice(settings.SHORTURL_PATH_ALPHABET) for _ in range(
                settings.SHORTURL_PATH_SIZE))

    @staticmethod
    def is_url_valid(myurl):
        rtn = True
        try:
            # workaroud for django 1.5.11 bug on %20 encoding causing urlvalidation to fail
            valid = _URL_VALIDATOR(Utils.get_decodedurl(myurl.replace("%20","_")))
        except:
            rtn = False
            pass
        return rtn

    @staticmethod
    def get_json(request, key):
        try:
            json_data = json.loads(request.body)
        except:
            json_data = None
            pass
        try:
            if json_data:
                if json_data[key]:
                    return json_data[key]
        except:
            pass
        return None

    @staticmethod
    def is_image(url):
        try:
            if mimetypes.guess_type(url)[0].split('/')[0] == 'image':
                return True
        except:
            pass
        return False

    @staticmethod
    def true_or_false(value):
        def switch(x):
            return {
                str(value)[0:1].upper() in ['T','Y','1']: True,
                str(value).upper() in ['TRUE','YES']: True,
                }.get(x, False)
        return switch(value)

    @staticmethod
    def get_meta(request, normalize):
        #
        # 1. User's IP address
        #
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR', 'unknown')
        #
        # 2. User's geolocation
        #
        slatlong = request.META.get('HTTP_X_APPENGINE_CITYLATLONG', '0.0,0.0')
        geo_lat = slatlong.split(',')[0]
        geo_long = slatlong.split(',')[1]
        geo_city = request.META.get('HTTP_X_APPENGINE_CITY', 'unknown')
        geo_country = request.META.get('HTTP_X_APPENGINE_COUNTRY','unknown')
        #
        # 3. Relevant, useful http headers
        #
        http_host = request.META.get('HTTP_HOST','unknown')
        http_useragent = request.META.get('HTTP_USER_AGENT', 'unknown')
        http_referer = request.META.get('HTTP_REFERER','unknown')
        if normalize:
            return ip_address.lower(), geo_lat, geo_long, geo_city.lower(), geo_country.lower(), http_host.lower(), http_useragent.lower(), http_referer.lower()
        else:
            return ip_address, geo_lat, geo_long, geo_city, geo_country, http_host, http_useragent, http_referer

    @staticmethod
    def remove_nonascii(value):
        if value is None:
            return None
        else:
            return "".join(filter(lambda x: ord(x)<128, value))

    @staticmethod
    def url_exists(url):
        rtn = False
        try:
            r = urllib2.urlopen(url)
            if r.code in (200, 401):
                rtn = True
        except:
            pass
        return rtn

    @staticmethod
    def get_geo_country_ordinal(geo_country):
        if geo_country == 'us':
            return 0
        else:
            return (1000 * ord(geo_country[0].lower())) + ord(geo_country[1].lower())

    @staticmethod
    def get_geo_city_ordinal(geo_city):
        c = geo_city.replace(' ','')
        def ggco_recurse(c, l, o):
            k = c[0:1]
            i = ord(k) - 96
            o = o + (i * 10**-l)
            l += 1
        if geo_country == 'us':
            return 0
        else:
            return
