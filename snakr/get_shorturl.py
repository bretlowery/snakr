# import hashlib
# import random
# import urllib
# import sys
# import re
# import json
from urlparse import urlparse, urlunparse
from utils import utils

class GetShortURL:
    """Validates and processes the short URL in the GET request."""
    shorturl = ''
    shorturl_is_preencoded = False
    normalized_shorturl = ''
    normalized_shorturl_parts = None

    def __init__(self, request):
        surl = request.build_absolute_uri()
        dsurl = utils.get_decodedurl(surl)
        sparts = urlparse(dsurl)
        if surl == dsurl:
            preencoded = False
        else:
            preencoded = True
            l = dsurl
        self.normalized_shorturl_parts = (
            sparts.scheme.lower(), sparts.netloc.lower(), sparts.path, sparts.params, sparts.query,
            sparts.fragment)
        self.shorturl_is_preencoded = preencoded
        self.normalized_shorturl = urlunparse(sparts)
        self.shorturl = surl
        return

#    def persist(self):

