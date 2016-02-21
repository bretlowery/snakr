import json
from urlparse import urlparse, parse_qs
import secure.settings as settings
from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from models import LongURLs, ShortURLs, savelog
from shorturls import ShortURL
from utils import utils
from django.db import transaction

class LongURL:
    """Validates and processes the long URL in the POST request."""

    def __init__(self, request):
        self.longurl = ""
        self.longurl_is_preencoded = False
        self.normalized_longurl = ""
        self.normalized_longurl_scheme = ""
        self.id = 0
        lurl = ""

        found = True
        try:
            json_data = json.loads(request.body)
        except:
            json_data = None
            pass
        found = False
        if json_data:
            lurl = json_data["u"]
            if not lurl:
                lurl_parts = urlparse(request.build_absolute_uri())
                if lurl_parts.query:
                    lurl = parse_qs(urlparse(request.build_absolute_uri()))["u"]
                    if lurl:
                        found = True
            else:
                found = True
        if not found:
            raise SuspiciousOperation('No long URL found to shorten. Long URLs must be passed into Snakr using either a JSON payload value with a key of "u", or via a querystring "u" parameter (e.g. /?u="the_url").')

        if lurl == utils.get_decodedurl(lurl):
            preencoded = False
            self.normalized_longurl = utils.get_encodedurl(lurl)
        else:
            preencoded = True
            self.normalized_longurl = lurl
        if not utils.is_url_valid(self.normalized_longurl):
            raise SuspiciousOperation(
                'The URL submitted for shortening ({%s}) is not a valid URL.' %
                self.normalized_longurl)

        self.normalized_longurl_scheme = urlparse(lurl).scheme.lower()
        self.longurl_is_preencoded = preencoded
        self.longurl = lurl
        self.id = utils.get_longurlhash(self.normalized_longurl)

        return

    def get_or_make_shorturl(self, request):
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
            s = ShortURL()
            s.make(self.normalized_longurl_scheme)
            compression_ratio = float(len(s.shorturl)) / float(len(self.normalized_longurl))
            #
            # 3. Create a matching ShortURLs persistence object
            #
            sdata = ShortURLs(id=s.id, longurl_id=ldata.id, shorturl=s.shorturl, is_active='Y',
                              compression_ratio=compression_ratio, shorturl_path_size=settings.SHORTURL_PATH_SIZE)
            #
            # 4. Persist everything
            #
            ldata.save()
            sdata.save()
            savelog(request, entry_type='N', longurl_id=ldata.id, shorturl_id=s.id)
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
                raise SuspiciousOperation(
                    'HASH COLLISION DETECTED on lookup of long URL {%s}' % self.normalized_longurl)
            #
            # 2. Lookup the short url
            #
            s = ShortURLs.objects.get(longurl_id=self.id, is_active='Y')
            if not s:
                raise Http404
            #
            # 3. Log the lookup
            #
            savelog(request, entry_type='R', longurl_id=self.id, shorturl_id=s.id)
            #
            # 4. Return the short url
            #
        return s.shorturl
