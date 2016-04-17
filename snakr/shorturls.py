'''
ShortURLs.py contains the logic necessary to take a short URL and redirect to its long URL equivalent. It also contains the logic
needed to construct a short URL when a long URL is submitted to Snakr.
'''
import secure.settings as settings
from urlparse import urlparse, urlunparse
from models import ShortURLs, LongURLs
from utilities import Utils
from django.db import transaction as xaction
import loggr

class ShortURL:
    """Validates and processes the short URL in the GET request."""

    def __init__(self, request, *args, **kwargs):
        self.shorturl = ''
        self.shorturl_is_preencoded = False
        self.normalized_shorturl = ''
        self.normalized_shorturl_scheme = ''
        self.id = -1
        self._event = loggr.SnakrEventLogger()
        return

    def make(self, normalized_longurl_scheme, vanity_path):
        #
        # Make a new short URL
        #
        if settings.MAX_RETRIES < 1 or settings.MAX_RETRIES > 3:
            raise self._event.log(messagekey='ILLEGAL_MAX_RETRIES', status_code=400)
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
        # 2. Make a short url.
        #    a. If vanity_path was passed, use it; otherwise:
        #    b. If no vanity path was passed, build a path with SHORTURL_PATH_SIZE characters from SHORTURL_PATH_ALPHABET.
        #    c. Does it exist already? If so, regenerate it and try again.
        #
        use_exact_vanity_path = False
        vp = ''
        if vanity_path:
            if vanity_path[0] == '!':
                use_exact_vanity_path = True
                vp = vanity_path[1:]
            else:
                use_exact_vanity_path = False
                vp = vanity_path
        shorturl_candidate = ''
        shash = 0
        i = 0
        sc = 1
        while i <= settings.MAX_RETRIES and sc != 0:
            i += 1
            if i <= settings.MAX_RETRIES:
                if use_exact_vanity_path:
                    shorturl_candidate = shorturl_prefix + vp
                elif vp:
                    shorturl_candidate = shorturl_prefix + vp + '-' + Utils.get_shortpathcandidate(digits_only=True)
                else:
                    shorturl_candidate = shorturl_prefix + Utils.get_shortpathcandidate()
                shash = Utils.get_shorturlhash(shorturl_candidate)
                s = ShortURLs.objects.filter(id=shash)
                sc = s.count()
                if use_exact_vanity_path:
                    if sc != 0:
                        raise self._event.log(messagekey='VANITY_PATH_EXISTS', status_code=400)
                    break

        if i > settings.MAX_RETRIES:
            raise self._event.log(messagekey='EXCEEDED_MAX_RETRIES', status_code=400)
        #
        # 3. SUCCESS! Complete it and return it as a ****decoded**** url (which it is at this point)
        #
        self.shorturl = shorturl_candidate
        self.normalized_shorturl = self.shorturl
        self.normalized_shorturl_scheme = normalized_longurl_scheme
        self.id = shash
        return self.normalized_shorturl

    @xaction.atomic
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
        dsurl = Utils.get_decodedurl(surl)
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
        #
        # Was the shorturl encoded or malcoded? If so, don't trust it.
        #
        if self.shorturl != self.normalized_shorturl:
            raise self._event.log(request=request, messagekey='SHORT_URL_ENCODING_MISMATCH', status_code=400)
        #
        # Lookup the short url
        #
        self.id = Utils.get_shorturlhash(self.normalized_shorturl)
        try:
            s = ShortURLs.objects.get(id = self.id)
            if not s:
                raise self._event.log(request=request, messagekey='SHORT_URL_NOT_FOUND', value=self.shorturl, status_code=400)
        except:
            raise self._event.log(request=request, messagekey='SHORT_URL_NOT_FOUND', value=self.shorturl, status_code=400)

        if s.shorturl != self.shorturl:
            raise self._event.log(request=request, messagekey='SHORT_URL_MISMATCH', status_code=400)
        #
        # If the short URL is not active, 404
        #
        if s.is_active != 'Y':
            raise self._event.log(request=request, messagekey='HTTP_404', value=self.shorturl, status_code=404)
        #
        # Lookup the matching long url by the short url's id.
        # If it doesn't exist, 404.
        # If it does, decode it.
        #
        l = LongURLs.objects.get(id = s.longurl_id)
        if not l:
            raise self._event.log(request=request, messagekey='HTTP_404', value='ERROR, HTTP 404 longurl not found', longurl_id=s.longurl_id, shorturl_id=self.id, shorturl=self.shorturl, status_code=422)
        longurl = Utils.get_decodedurl(l.longurl)
        #
        # Log that a 302 request to the matching long url is about to occur
        #
        self._event.log(request=request, event_type='S', messagekey='HTTP_302', value=self.shorturl, longurl_id=s.longurl_id, longurl=longurl, shorturl_id=self.id, shorturl=self.shorturl, status_code=302)
        #
        # Return the longurl
        #
        return longurl

