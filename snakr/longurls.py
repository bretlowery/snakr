import json
from urlparse import urlparse, urlunparse
from django.core.exceptions import SuspiciousOperation
from utils import utils
from models import LongURLs, ShortURLs, savelog
from shorturls import ShortURL
import web.settings as settings
from django.db import transaction


class LongURL:
    """Validates and processes the long URL in the POST request."""
    longurl = ''
    longurl_is_preencoded = False
    normalized_longurl = ''
    normalized_longurl_scheme = ''
    id = 0

    def __init__(self, request):
        json_data = json.loads(request.body)
        lurl=''
        if json_data:
            lurl = json_data["u"]
        if not lurl:
            raise SuspiciousOperation('Required JSON "u" keyvalue pair not found in the POST request.')
        dlurl = utils.get_decodedurl(lurl)
        if not utils.is_url_valid(dlurl):
            raise SuspiciousOperation('The URL found in the JSON "u" data value ("%s") in the POST request is not a valid URL.' % dlurl)
        lparts = urlparse(dlurl)
        if lurl == dlurl:
            preencoded = False
        else:
            preencoded = True
            l = dlurl
        self.normalized_longurl_scheme = lparts.scheme.lower()
        self.longurl_is_preencoded = preencoded
        self.normalized_longurl = urlunparse(lparts)
        self.longurl = lurl
        self.id = utils.get_longurlhash(self.normalized_longurl)
        return

    @transaction.commit_on_success
    def persist(self, request):
        #
        # Does the long URL already exist?
        #
        l = LongURLs.objects.filter(id=self.id)
        lc = l.count()
        if lc == 0:
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
            s.make_shorturl(self.normalized_longurl_scheme)
            compression_ratio = float(len(s.shorturl)) / float(len(self.normalized_longurl))
            #
            # 3. Create a matching ShortURLs persistence object
            #
            sdata = ShortURLs(id=s.id, longurl_id=ldata.id, shorturl=s.shorturl, is_active='Y',
                              compression_ratio=compression_ratio, shorturl_path_size=settings.SHORTURL_PATH_SIZE)
            #
            # 4. Persist everything
            #
            # dberror = False
            # try:
            ldata.save()
            sdata.save()
            savelog(request, entry_type='NL', longurl_id=ldata.id, shorturl_id=s.id)
            # except:
            #     transaction.rollback()
            #     dberror = True
            # if not dberror:
            #     transaction.commit()
            #
            # 6. Return the short url
            #
            return s.shorturl
        else:
            if l.longurl != self.normalized_longurl:
                raise SuspiciousOperation('HASH COLLISION DETECTED on lookup of long URL <%s>' % self.normalized_longurl)

        return
