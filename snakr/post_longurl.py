import hashlib
import random
import urllib
import sys
import re
import json
from urlparse import urlparse, urlunparse

from django.http import HttpResponseBadRequest

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

class PostLongURL:
    """Validation class to vaidate that the POST request to the service has a valid JSON payload and
    is properly formatted, escaped and minimally secured."""

    def __init__(self, request):
        self.longurl = ''
        self.longurl_is_preencoded = False
        self.normalized_longurl = ''
        self.normalized_longurl_parts = None
        json_data = json.loads(request.body)
        if not json_data:
            raise BadPostRequest(message_text='Required JSON data not found in the POST request.')
        lurl = json_data["u"]
        if not lurl:
            raise BadPostRequest(message_text='Required JSON "u" keyvalue pair not found in the POST request.')
        dlurl = utils.get_decodedurl(lurl)
        if not utils.is_url_valid(dlurl):
            raise BadPostRequest(message_text='The URL found in the JSON "u" data value in the POST request is not a valid URL.')
        lparts = urlparse(dlurl)
        if lurl == dlurl:
            preencoded = False
        else:
            preencoded = True
            l = dlurl
        lparts.scheme = lparts.scheme.lower()
        lparts.netloc = lparts.netloc.lower()
        self.normalized_longurl_parts = (
            lparts.scheme, lparts.netloc, lparts.path, lparts.params, lparts.query,
            lparts.fragment)
        self.longurl_preencoded = preencoded
        self.normalized_longurl = urlunparse(lparts)
        self.longurl = lurl
        return

