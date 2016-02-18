from urlparse import urlparse, urlunparse

from django.core.exceptions import SuspiciousOperation

import web.settings as settings
from models import ShortURLs
from utils import utils


class ShortURL:
    """Validates and processes the short URL in the GET request."""
    shorturl = ''
    shorturl_is_preencoded = False
    normalized_shorturl = ''
    normalized_shorturl_scheme = ''
    id = 0

    def __init__(self):
        return

    def make_shorturl(self, normalized_longurl_scheme):
        if settings.MAX_RETRIES < 1:
            raise SuspiciousOperation('ERROR, MAX_RETRIES must be >= 1, but is actually set to %d' % settings.MAX_RETRIES)
        #
        # Makes a short URL
        #
        # 1. Build the front of the short url. Match the scheme to the one used by the longurl.
        #    This is done so that a http longurl --> http shorturl, and a https long url --> https short url.
        #
        shorturl_prefix = normalized_longurl_scheme + '://' + settings.SHORTURL_HOST + '/'
        #
        # 2. Make a short url with SHORTURL_PATH_SIZE characters from SHORTURL_PATH_ALPHABET. Does it exist already?
        #    If so, regenerate it and try again.
        #
        shorturl_candidate = ''
        shash = 0
        i = 0
        sc = 1
        while i <= settings.MAX_RETRIES and sc != 0:
            i += 1
            if i <= settings.MAX_RETRIES:
                shorturl_candidate = shorturl_prefix + utils.get_shorturlcandidate()
                shash = utils.get_shorturlhash(shorturl_candidate)
                s = ShortURLs.objects.filter(id=shash)
                sc = s.count()
        if i > settings.MAX_RETRIES:
            raise SuspiciousOperation('ERROR, exceeded %d tries to generate new short URL.' % settings.MAX_RETRIES)
        #
        # 3. SUCCESS! Complete it and return it as a ****decoded**** url (which it is at this point)
        #
        self.shorturl = shorturl_candidate
        self.normalized_shorturl = self.shorturl
        self.normalized_shorturl_scheme = normalized_longurl_scheme
        self.id = shash
        return

    def validate(self, request):
        surl = request.build_absolute_uri()
        dsurl = utils.get_decodedurl(surl)
        sparts = urlparse(dsurl)
        if surl == dsurl:
            preencoded = False
        else:
            preencoded = True
            l = dsurl
        self.normalized_longurl_scheme = sparts.scheme.lower()
        self.shorturl_is_preencoded = preencoded
        self.normalized_shorturl = urlunparse(sparts)
        self.shorturl = surl
        self.id = utils.get_longurlhash(self.normalized_shorturl)
        return



