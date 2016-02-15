import hashlib
import random
import urllib
import sys
import re
import json
from urlparse import urlparse, urlunparse

from django.http import HttpResponseBadRequest, HttpRequest

from utils import utils

class BadPostRequest(HttpResponseBadRequest):
    status_code = 400
    message_text = 'Unknown error in POST request'

    def __init__(self, *args, **kwargs):
        super(HttpResponseBadRequest, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<%(cls)s [status_code=%(status_code)d, "%(content_type)s", "%(message_text)s">' % {
            'cls': self.__class__.__name__,
            'status_code': self.status_code,
            'content_type': self['Content-Type'],
            'message_text': self.message_text,
        }


class GetShortURL:
    """Validates and processes the short URL in the GET request."""
    shorturl = ''
    shorturl_is_preencoded = False
    normalized_shorturl = ''
    normalized_shorturl_parts = None

    def __init__(self, request):
        surl = request.build_absolute_uri()
        dsurl = utils.get_decodedurl(surl)
        lparts = urlparse(dsurl)
        if surl == dsurl:
            preencoded = False
        else:
            preencoded = True
            l = dsurl
        self.normalized_shorturl_parts = (
            lparts.scheme.lower(), lparts.netloc.lower(), lparts.path, lparts.params, lparts.query,
            lparts.fragment)
        self.shorturl_is_preencoded = preencoded
        self.normalized_shorturl = urlunparse(lparts)
        self.shorturl = surl
        return


