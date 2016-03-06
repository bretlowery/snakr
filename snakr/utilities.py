import hashlib
import random
import urllib
from urlparse import urlparse
import secure.settings as settings
from django.core.validators import URLValidator
import json
import mimetypes

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
    def get_hash(str):
        """Returns a SHA1 hash of the passed string as-encoded"""
        if str == 'unknown':
            x = 0
        else:
            x = long(hashlib.sha1(str).hexdigest(),16)
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
    def initurlparts():
        return urlparse('http://www.dummyurl.com')  # this is a django 1.5.11 bug workaround

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