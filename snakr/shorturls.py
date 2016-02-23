import secure.settings as settings
from urlparse import urlparse, urlunparse
from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from models import ShortURLs, LongURLs, writelog
from utils import utils
# from django.db import transaction

class ShortURL:
    """Validates and processes the short URL in the GET request."""

    def __init__(self, *args, **kwargs):
        self.shorturl = ''
        self.shorturl_is_preencoded = False
        self.normalized_shorturl = ''
        self.normalized_shorturl_scheme = ''
        self.id = -1

    def make(self, normalized_longurl_scheme):
        #
        # Make a new short URL
        #
        if settings.MAX_RETRIES < 1:
            raise SuspiciousOperation('ERROR, MAX_RETRIES must be >= 1, but is actually set to %d' % settings.MAX_RETRIES)
        #
        # Makes a short URL
        #
        # 1. Build the front of the short url. Match the scheme to the one used by the longurl.
        #    This is done so that a http longurl --> http shorturl, and a https long url --> https short url.
        #
        if normalized_longurl_scheme in ('https','ftps','sftp'):
            shorturl_prefix = normalized_longurl_scheme + '://' + settings.SECURE_SHORTURL_HOST + '/'
        else:
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
        return self.normalized_shorturl

    def getlongurl(self, request):
        self.shorturl = ''
        self.shorturl_is_preencoded = False
        self.normalized_shorturl = ''
        self.normalized_shorturl_scheme = ''
        self.id = -1
        #
        # cleanse the passed short url
        #
        surl = request.build_absolute_uri()
        dsurl = utils.get_decodedurl(surl)
        sparts = urlparse(dsurl)
        if surl == dsurl:
            preencoded = False
        else:
            preencoded = True
            l = dsurl
        self.normalized_shorturl_scheme = sparts.scheme.lower()
        self.shorturl_is_preencoded = preencoded
        self.normalized_shorturl = urlunparse(sparts)
        if self.normalized_shorturl.endswith("/"):
            self.normalized_shorturl = self.normalized_shorturl[:-1]
        self.shorturl = surl
        if self.shorturl.endswith("/"):
            self.shorturl = self.shorturl[:-1]
        #
        # If no path provided, redirect to the defined index.html
        #
        if sparts.path == '/':
            return settings.INDEX_HTML
            # raise SuspiciousOperation('ERROR: the short URL provided is incomplete. Please provide a valid, unmodified short URL previously generated by this service.')
        #
        # Ensure there's a valid path to begin with
        #
        if sparts.query or not utils.is_validnsp(sparts.path):
            raise SuspiciousOperation('ERROR: the short URL sent to this service is different from the original short URL provided and may pose a security risk. DO NOT USE the altered version.')
        #
        # Was the shorturl encoded or malcoded? If so, don't trust it.
        #
        if self.shorturl != self.normalized_shorturl:
            raise SuspiciousOperation('ERROR: the short URL sent to this service is encoded differently from the original short URL provided and may pose a security risk. DO NOT USE the altered version.')
        self.id = utils.get_shorturlhash(self.normalized_shorturl)
        #
        # Lookup the short url
        #
        # raise SuspiciousOperation('{%s} {%s} {%s}' % (self.id, self.shorturl,self.normalized_shorturl))
        try:
            s = ShortURLs.objects.get(id = self.id)
            if not s:
                raise SuspiciousOperation('ERROR: URL {%s} is not recognized by this service.' % self.shorturl)
        except:
            raise SuspiciousOperation('ERROR: URL {%s} is not recognized by this service.' % self.shorturl)
        if s.shorturl != self.shorturl:
            raise SuspiciousOperation('ERROR: the short URL sent to this service is different from the original short URL provided and may pose a security risk. DO NOT USE the altered version.')
        #
        # If the short URL is not active, 404
        #
        if s.is_active != 'Y':
            raise Http404
        # Lookup the matching long url by the short url's id.
        # If it doesn't exist, 404.
        # If it does, decode it.
        #
        l = LongURLs.objects.get(id = s.longurl_id)
        if not l:
            raise Http404
        longurl = utils.get_decodedurl(l.longurl)
        #
        # Log that a 302 request to the matching long url is about to occur
        #
        writelog(request, entry_type='S', longurl_id=s.longurl_id, shorturl_id=self.id)
        #
        # Return the longurl
        #
        return longurl

