'''
LongURLs.py contains the logic necessary to consume a long URL and return a short URL for it.
'''
from urlparse import urlparse, parse_qs
import secure.settings as settings
from django.http import Http404
from models import LongURLs, ShortURLs
from shorturls import ShortURL
from utilities import utils
from django.db import transaction as xaction
import loggr

class LongURL:
    """Validates and processes the long URL in the POST request."""

    def __init__(self, request, *args, **kwargs):
        self.longurl = ""
        self.longurl_is_preencoded = False
        self.normalized_longurl = ""
        self.normalized_longurl_scheme = ""
        self.id = 0
        self.vanity_path = ''
        self.event = loggr.SnakrEventLogger()

        lurl = ""

        lurl = utils.get_json(request, 'u')
        if not lurl:
            raise self.event.log(messagekey='LONG_URL_MISSING', status_code=400)

        if not utils.is_url_valid(lurl):
            raise self.event.log(messagekey='LONG_URL_INVALID', value=lurl, status_code=400)

        self.vanity_path = utils.get_json(request, 'vp')

        if lurl == utils.get_decodedurl(lurl):
            preencoded = False
            self.normalized_longurl = utils.get_encodedurl(lurl)
        else:
            preencoded = True
            self.normalized_longurl = lurl

        self.normalized_longurl_scheme = urlparse(lurl).scheme.lower()
        self.longurl_is_preencoded = preencoded
        self.longurl = lurl
        self.id = utils.get_longurlhash(self.normalized_longurl)

        return

    @xaction.atomic
    def get_or_make_shorturl(self, request, *args, **kwargs):
        nopersist = utils.get_json(request, 'nopersist')
        #
        # Does the long URL already exist?
        #
        try:
            l = LongURLs.objects.get(id=self.id)
        except:
            l = None
            pass
        if not l:
            #
            # NO IT DOESN'T
            #
            # 1. Create a LongURLs persistence object
            #
            if self.longurl_is_preencoded:
                originally_encoded = 'Y'
            else:
                originally_encoded = 'N'
            ldata = LongURLs(id=self.id, longurl=self.normalized_longurl, originally_encoded=originally_encoded)
            #
            # 2. Generate a short url for it (with collision handling) and calc its compression ratio vs the long url
            #
            s = ShortURL(request)
            s.make(self.normalized_longurl_scheme, self.vanity_path)
            compression_ratio = float(len(s.shorturl)) / float(len(self.normalized_longurl))
            #
            # 3. Create a matching ShortURLs persistence object
            #
            sdata = ShortURLs(id=s.id, longurl_id=ldata.id, shorturl=s.shorturl, is_active='Y',
                              compression_ratio=compression_ratio, shorturl_path_size=settings.SHORTURL_PATH_SIZE)
            #
            # 4. Persist everything
            #
            if not nopersist:
                ldata.save()
                sdata.save()
                self.event.log(event_type='L', messagekey='HTTP_200', value=self.normalized_longurl, longurl_id=self.id, shorturl_id=s.id, status_code=200)
            #
            # 5. Return the short url
            #
        else:
            #
            # YES IT DOES
            # Return the existing short url to the caller
            #
            # 1. Check for potential collision
            #
            if l.longurl != self.normalized_longurl:
                raise self.event.log(messagekey='HASH_COLLISION', value=self.normalized_longurl, status_code=400)
            #
            # 2. Lookup the short url. It must be active.
            #
            s = ShortURLs.objects.get(longurl_id=self.id, is_active='Y')
            if not s:
                raise Http404
            #
            # 3. Log the lookup
            #
            self.event.log(event_type='R', messagekey='LONG_URL_RESUBMITTED', value=self.normalized_longurl, longurl_id=self.id, shorturl_id=s.id, status_code=200)
            #
            # 4. Return the short url
            #
        return s.shorturl
