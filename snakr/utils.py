import urllib
import hashlib
import re
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
    def get_urlhash(myurl):
        """Returns a SHA1 hash of the encoded version of the passed URL."""
        return hashlib.sha1(urllib.quote(myurl).encode('utf8')).hexdigest()

    @staticmethod
    def is_url_valid(myurl):
        rtn = True
        try:

            dummy = _URL_VALIDATOR(myurl)
        except:
            rtn = False
            pass
        return rtn
