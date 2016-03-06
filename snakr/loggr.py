'''
Centralized event logging for Snakr. Wraps the Django core logging system and adds JSON logging support.
'''
import logging
from pythonjsonlogger import jsonlogger
import datetime
import secure.settings as settings
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpResponseServerError, HttpRequest
from patterns.singleton import Singleton


class SnakrEventLogger(Exception):

    _ENTRY_TYPE = (
        ('I', 'Information'),
        ('L', 'New Long URL Submitted'),
        ('S', 'Short URL 302'),
        ('R', 'Existing Long URL Resubmitted'),
        ('X', 'Exception'),
        ('E', 'Error'),
        ('W', 'Warning'),
        ('D', 'Debug'),
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
        entry_type = kwargs.pop('entry_type', 'W')
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
            #
            # 1. User's IP address
            #
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR', 'unknown')
            #
            # 2. User's geolocation
            #
            slatlong = request.META.get('HTTP_X_APPENGINE_CITYLATLONG', '0.0,0.0')
            geo_lat = slatlong.split(',')[0]
            geo_long = slatlong.split(',')[1]
            geo_city = request.META.get('HTTP_X_APPENGINE_CITY', 'unknown')
            geo_country = request.META.get('HTTP_X_APPENGINE_COUNTRY','unknown')
            #
            # 3. Relevant, useful http headers
            #
            http_host = request.META.get('HTTP_HOST','unknown')
            http_user_agent = request.META.get('HTTP_USER_AGENT','unknown')
            http_referer = request.META.get('HTTP_REFERER','unknown')
        #
        #
        #
        if entry_type == 'I':
            status_code = 0
        if status_code == 200 and entry_type == 'W':
            entry_type = 'I'
        if status_code not in (0,200,400,404,422,500):
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
            info = info % value

        dupe_message = False
        if request:
            if ip_address == self.last_ip_address:
                if http_user_agent == self.last_http_user_agent:
                    if dtnow == self.last_dtnow:
                        dupe_message = True

        if not dupe_message:

            jsondata = {}
            if verbose and request:
                jsondata = {
                    'snakr':    dtnow,
                    'type':     entry_type,
                    'code':     str(status_code),
                    'lid':      str(longurl_id),
                    'sid':      str(shorturl_id),
                    'ip':       ip_address,
                    'lat':      str(geo_lat),
                    'long':     str(geo_long),
                    'city':     str(geo_city),
                    'cnty':     str(geo_country),
                    'host':     str(http_host),
                    'ua':       str(http_user_agent),
                }
            else:
                jsondata = {
                    'snakr':    dtnow,
                    'type':     entry_type,
                    'code':     str(status_code),
                }
            if (status_code <= 200 and settings.LOG_HTTP200) or (status_code == 404 and settings.LOG_HTTP404) or (status_code == 302 and settings.LOG_HTTP302):
                self.logger.info(info, extra=jsondata)
            elif status_code == 400 and settings.LOG_HTTP400:
                self.logger.warning(info, extra=jsondata)
            else:
                self.logger.critical(info, extra=jsondata)

            def switch(x):
                return {
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