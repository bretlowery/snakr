'''
Centralized event logging for Snakr. Wraps the Django core logging system and adds JSON logging support.
'''
import logging
from pythonjsonlogger import jsonlogger
import datetime
import secure.settings as settings
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.http import Http404, HttpResponseServerError, HttpRequest
from patterns.singleton import Singleton
from utilities import Utils
from django.db import transaction as xaction

class SnakrEventLogger(Exception):

    _ENTRY_TYPE = (
        ('B', '403 Bot/Blacklisted'),
        ('D', 'Debug'),
        ('E', 'Error'),
        ('I', 'Information'),
        ('L', '200 New Long URL Submitted'),
        ('R', '200 Existing Long URL Resubmitted'),
        ('S', '302 Short URL Redirect'),
        ('W', 'Warning'),
        ('X', 'Exception'),
    )

    def __init__(self, *args, **kwargs):
        #
        # there can be only one
        # to minimize the duplication of messages that Django is known for
        # see Method 3 on http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
        #
        __metaclass__ = Singleton
        #
        # initialize python-json-logger
        # see: https://github.com/madzak/python-json-logger
        #
        self.logger = logging.getLogger(settings.GAE_PROJECT_ID)
        if settings.VERBOSE_LOGGING:
            self.logger.handlers = []
            self.__logHandler = logging.StreamHandler()
            self.__formatter = jsonlogger.JsonFormatter()
            self.__logHandler.setFormatter(self.__formatter)
            self.logger.addHandler(self.__logHandler)
            self.__last = None
        self.last_ip_address = 'N/A'
        self.last_dtnow = 'N/A'
        self.last_http_user_agent = 'N/A'
        return

    def log(self, **kwargs):
        #
        # get parameters
        #
        if not settings.ENABLE_LOGGING:
            return
        request = kwargs.pop("request", None)
        if not isinstance(request, HttpRequest):
            request = None
        infokey = kwargs.pop('messagekey', None)
        info = kwargs.pop('message', None)
        try:
            value = str(kwargs.pop('value', None))
        except:
            value = None
            pass
        event_type = kwargs.pop('event_type', 'W')
        longurl_id = kwargs.pop('longurl_id', -1)
        shorturl_id = kwargs.pop('shorturl_id', -1)
        verbose = kwargs.pop('verbose', False)
        status_code = kwargs.pop('status_code', 200)
        dt = datetime.datetime.now()
        dtnow = kwargs.pop('dt', dt.isoformat())
        #
        # get client info from the request objext
        #
        if request:
            ip_address, geo_lat, geo_long, geo_city, geo_country, http_host, http_useragent, http_referer = Utils.get_meta(request, False)
        #
        if event_type == 'I':
            status_code = 0
        if status_code == 200:
            event_type = 'I'
        if status_code not in (-403,0,200,400,404,422,500):
            status_code = 403
        if settings.DEBUG or settings.VERBOSE_LOGGING or (status_code >= 400 and status_code != 404):
            verbose = True
        if not info:
            if infokey:
                infokey = infokey.strip().upper()
                try:
                    info = settings.CANONICAL_MESSAGES[infokey]
                    if not info:
                        info = settings.MESSAGE_OF_LAST_RESORT
                except:
                    info = settings.MESSAGE_OF_LAST_RESORT
                    pass
            else:
                info = settings.MESSAGE_OF_LAST_RESORT
        if value is not None and value != 'None':
            if info:
                try:
                    info = info % value
                except:
                    info = value
                    pass
            else:
                info = value

        dupe_message = False
        if request:
            if ip_address == self.last_ip_address:
                if http_useragent == self.last_http_user_agent:
                    if dtnow == self.last_dtnow:
                        dupe_message = True

        if not dupe_message:

            jsondata = {
                'snakr':    dtnow,
                'type':     event_type,
                'code':     str(status_code),
            }

            db_id = -1
            if settings.DATABASE_LOGGING and request:
                db_id = self._log_transaction(dt, event_type, status_code, info, shorturl_id, longurl_id, ip_address, geo_lat, geo_long, geo_city, geo_country, http_host, http_useragent)
                jsondata['snakr_eventlog_id'] = str(db_id)

            if (settings.VERBOSE_LOGGING or verbose) and request:
                    jsondata['lid'] = str(longurl_id)
                    jsondata['sid'] = str(shorturl_id)
                    jsondata['ip'] = ip_address
                    jsondata['lat'] = str(geo_lat)
                    jsondata['long'] = str(geo_long)
                    jsondata['city'] = str(geo_city)
                    jsondata['cnty'] = str(geo_country)
                    jsondata['host'] = str(http_host)
                    jsondata['ua'] = str(http_useragent)
                    jsondata['ref'] = http_referer

            if abs(status_code) == 403 and settings.LOG_HTTP403:
                self.logger.warning(info, extra=jsondata)
            elif (status_code <= 200 and settings.LOG_HTTP200) or (status_code == 404 and settings.LOG_HTTP404) or (status_code == 302 and settings.LOG_HTTP302):
                self.logger.info(info, extra=jsondata)
            elif status_code == 400 and settings.LOG_HTTP400:
                self.logger.warning(info, extra=jsondata)
            else:
                self.logger.critical(info, extra=jsondata)

            def switch(x):
                return {
                    -403:PermissionDenied,
                    200: info,
                    302: info,
                    400: SuspiciousOperation(info),
                    403: SuspiciousOperation(info),
                    404: Http404,
                    422: SuspiciousOperation(info),
                    500: HttpResponseServerError(info),
                }.get(x, 200)

            if status_code != 0:
                return switch(status_code)

        return

    @xaction.atomic
    def _log_transaction(self, dt, event_type, status_code, info, shorturl_id, longurl_id, ip_address, geo_lat, geo_long, geo_city, geo_country, http_host, http_useragent ):

        # imports here to keep their code within the scope of the transaction
        from snakr.models import EventLog, UserAgentLog, HostLog, CityLog, CountryLog, IPLog

        # dimension save helper function here to keep it within the scope of the transaction
        def _save_dimension(modelclass, value):
            if value:
                normalized_value =  ' '.join(str(value).split()).lower()
                hash_key = Utils.get_hash(normalized_value)
                if not modelclass.objects.filter(id=hash_key).exists():
                    dimension = modelclass(hash_key, normalized_value, 'N')
                    dimension.save()
            else:
                hash_key = 0
            return hash_key

        city_hash       = _save_dimension(CityLog, geo_city)
        country_hash    = _save_dimension(CountryLog, geo_country)
        host_hash       = _save_dimension(HostLog, http_host)
        useragent_hash  = _save_dimension(UserAgentLog, http_useragent)
        ip_hash         = _save_dimension(IPLog, ip_address)

        e = EventLog(
                logged_on=dt,
                event_type=event_type,
                http_status_code=status_code,
                message=info,
                longurl_id=longurl_id,
                shorturl_id=shorturl_id,
                ip_id=ip_hash,
                lat=geo_lat,
                lng=geo_long,
                city_id=city_hash,
                country_id=country_hash,
                host_id = host_hash,
                useragent_id=useragent_hash
        )

        e.save()
        return e.id

