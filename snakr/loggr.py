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
import googledatastore

class SnakrEventLogger(Exception):

    _ENTRY_TYPE = settings.EVENT_TYPES

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
        request = kwargs.pop('request', None)
        if not isinstance(request, HttpRequest):
            request = None
        messagekey = kwargs.pop('messagekey', None)
        message = kwargs.pop('message', None)
        if not message:
            if messagekey: 
                messagekey = messagekey.strip().upper()
                try:
                    message = settings.CANONICAL_MESSAGES[messagekey]
                    if not message:
                        message = settings.MESSAGE_OF_LAST_RESORT
                except:
                    message = settings.MESSAGE_OF_LAST_RESORT
                    pass
            else:
                message = settings.MESSAGE_OF_LAST_RESORT
        try:
            value = str(kwargs.pop('value', 'none'))
        except:
            value = None
            pass
        if value is not None and value != 'none':
            if message:
                try:
                    message = message % value
                except:
                    message = value
                    pass
            else:
                message = value
        event_type = kwargs.pop('event_type', 'W')
        longurl_id = kwargs.pop('longurl_id', -1)
        longurl = kwargs.pop('longurl', 'none')
        shorturl_id = kwargs.pop('shorturl_id', -1)
        shorturl = kwargs.pop('shorturl', 'none')
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
        #if status_code == 200:
        #    event_type = 'I'
        if status_code not in (-403,0,200,302,400,404,422,500):
            status_code = 403
        if settings.DEBUG or settings.VERBOSE_LOGGING or (status_code >= 400 and status_code != 404):
            verbose = True

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

            if settings.DATABASE_LOGGING and request:

                sql_id, ds_id = self._log_transaction(
                        jsondata = jsondata,
                        dt = dt,
                        event_type = event_type,
                        status_code = status_code,
                        message = message,
                        shorturl_id = shorturl_id,
                        shorturl = shorturl,
                        longurl_id = longurl_id,
                        longurl = longurl,
                        ip_address = ip_address,
                        geo_lat = geo_lat,
                        geo_long = geo_long,
                        geo_city = geo_city,
                        geo_country = geo_country,
                        http_host = http_host,
                        http_useragent = http_useragent
                )
                jsondata['snakr_cloudsql_eventlog_id'] = str(sql_id)
                jsondata['snakr_datastore_eventstream_id'] = str(ds_id)

            if abs(status_code) == 403 and settings.LOG_HTTP403:
                self.logger.warning(message, extra=jsondata)
            elif (status_code <= 200 and settings.LOG_HTTP200) or (status_code == 404 and settings.LOG_HTTP404) or (status_code == 302 and settings.LOG_HTTP302):
                self.logger.info(message, extra=jsondata)
            elif status_code == 400 and settings.LOG_HTTP400:
                self.logger.warning(message, extra=jsondata)
            else:
                self.logger.critical(message, extra=jsondata)

            def switch(x):
                return {
                    -403:PermissionDenied,
                    200: message,
                    302: message,
                    400: SuspiciousOperation(message),
                    403: SuspiciousOperation(message),
                    404: Http404,
                    422: SuspiciousOperation(message),
                    500: HttpResponseServerError(message),
                }.get(x, 200)

            if status_code != 0:
                return switch(status_code)

        return

    @xaction.atomic
    def _log_transaction(self, **kwargs):
        jsondata = kwargs.pop('jsondata', None)
        dt = kwargs.pop('dt',  datetime.datetime.now().isoformat())
        event_type = kwargs.pop('event_type', None)
        status_code = kwargs.pop('status_code', None)
        message = kwargs.pop('message', None)
        shorturl_id = kwargs.pop('shorturl_id', -1)
        shorturl = kwargs.pop('shorturl', None)
        longurl_id = kwargs.pop('longurl_id', -1)
        longurl = kwargs.pop('longurl', None)
        ip_address = kwargs.pop('ip_address', None)
        geo_lat = kwargs.pop('geo_lat', 0.0)
        geo_long = kwargs.pop('geo_long', 0.0)
        geo_city = kwargs.pop('geo_city', None)
        geo_country = kwargs.pop('geo_country', None)
        http_host = kwargs.pop('http_host', None)
        http_useragent = kwargs.pop('http_useragent', None)

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

        city_hash = _save_dimension(CityLog, geo_city)
        country_hash = _save_dimension(CountryLog, geo_country)
        host_hash = _save_dimension(HostLog, http_host)
        useragent_hash = _save_dimension(UserAgentLog, http_useragent)
        ip_hash = _save_dimension(IPLog, ip_address)

        sql_id = -1
        ds_id = -1

        if settings.PERSIST_EVENTSTREAM_TO_CLOUDSQL:

            # self.logger.info('Persisting event to Cloud SQL', extra=jsondata)
            e = EventLog(
                    logged_on=dt,
                    event_type=event_type,
                    http_status_code=abs(status_code),
                    message=message,
                    longurl_id=longurl_id,
                    shorturl_id=shorturl_id,
                    ip_id=ip_hash,
                    lat=geo_lat,
                    lng=geo_long,
                    city_id=city_hash,
                    country_id=country_hash,
                    host_id=host_hash,
                    useragent_id=useragent_hash
            )

            e.save()
            sql_id = e.id

        if settings.PERSIST_EVENTSTREAM_TO_DATASTORE:

            # self.logger.info('Persisting event to Datastore', extra=jsondata)
            gds = googledatastore.client()
            ds_id = gds.persist(
                    event_type=event_type,
                    http_status_code=abs(status_code),
                    info=message,
                    longurl=longurl,
                    shorturl=shorturl,
                    ip_address=ip_address,
                    geo_lat=geo_lat,
                    geo_long=geo_long,
                    geo_city=geo_city,
                    geo_country=geo_country,
                    http_host=http_host,
                    http_useragent=http_useragent
            )

        return sql_id, ds_id


