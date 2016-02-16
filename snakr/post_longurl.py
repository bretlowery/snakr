# import hashlib
# import random
# import urllib
# import sys
# import re
import json
from urlparse import urlparse, urlunparse
#from django.http import HttpResponseBadRequest
from django.core.exceptions import SuspiciousOperation
from utils import utils
from django.core.validators import URLValidator

class PostLongURL:
    """Validates and processes the long URL in the POST request."""
    longurl = ''
    longurl_is_preencoded = False
    normalized_longurl = ''
    normalized_longurl_parts = None

    def __init__(self, request):
        json_data = json.loads(request.body)
        if not json_data:
            raise SuspiciousOperation('Required JSON data not found in the POST request.')
        lurl = json_data["u"]
        if not lurl:
            raise SuspiciousOperation('Required JSON "u" keyvalue pair not found in the POST request.')
        dlurl = utils.get_decodedurl(lurl)
        if utils.is_url_valid(dlurl):
            raise SuspiciousOperation('The URL found in the JSON "u" data value ("%s") in the POST request is not a valid URL.' % dlurl)
        lparts = urlparse(dlurl)
        if lurl == dlurl:
            preencoded = False
        else:
            preencoded = True
            l = dlurl
        self.normalized_shorturl_parts = (
            lparts.scheme.lower(), lparts.netloc.lower(), lparts.path, lparts.params, lparts.query,
            lparts.fragment)
        self.shorturl_is_preencoded = preencoded
        self.normalized_shorturl = urlunparse(lparts)
        self.shorturl = lurl
        return

