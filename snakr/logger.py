import secure.settings as settings
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpResponseServerError, HttpRequest
import logging
from pythonjsonlogger import jsonlogger
import datetime

class Loggr(Exception):

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

    def __init__(self, *args):
        if len(args) == 1:
            request = args[0]
            if not isinstance(request, HttpRequest):
                request = None
        else:
            request = None
        #
        # initialize pythonjsonlogger
        # see: https://github.com/madzak/python-json-logger
        #
        self.logger = logging.getLogger()
        self.__logHandler = logging.StreamHandler()
        self.__formatter = jsonlogger.JsonFormatter()
        self.__logHandler.setFormatter(self.__formatter)
        self.logger.addHandler(self.__logHandler)
        #
        if request:
            #
            #
            # get client info from the request objext
            #
            # 1. User's IP address
            #
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                self.ip_address = x_forwarded_for.split(',')[0]
            else:
                self.ip_address = request.META.get('REMOTE_ADDR', 'unknown')
            #
            # 2. User's geolocation
            #
            slatlong = request.META.get('HTTP_X_APPENGINE_CITYLATLONG', '0.0,0.0')
            self.geo_lat = slatlong.split(',')[0]
            self.geo_long = slatlong.split(',')[1]
            self.geo_city = request.META.get('HTTP_X_APPENGINE_CITY', 'unknown')
            self.geo_country = request.META.get('HTTP_X_APPENGINE_COUNTRY','unknown')
            #
            # 3. Relevant, useful http headers
            #
            self.http_host = request.META.get('HTTP_HOST','unknown')
            self.http_user_agent = request.META.get('HTTP_USER_AGENT','unknown')
            self.http_referer = request.META.get('HTTP_REFERER','unknown')
        #
        return


    def event(self, **kwargs):

        if settings.ENABLE_LOGGING != True:
            return

        messagekey = kwargs.pop('messagekey', None)
        message = kwargs.pop('message', None)
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

        if entry_type == 'I':
            status_code = 0

        if status_code not in (0,200,400,404,422,500):
            status_code = 403

        if settings.DEBUG:
            verbose = True

        snakr_version = settings.__SNAKR__VERSION__
        jsondata = {"snakrlog": snakr_version}
        dt = datetime.datetime.now()
        jsondata['dt'] = dt.isoformat()
        jsondata['type'] = entry_type

        if verbose or longurl_id != -1:
            jsondata['lid'] = str(longurl_id)

        if verbose or shorturl_id != -1:
            jsondata['sid'] = str(shorturl_id)

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

        if value != None and value != 'None':
            message = message % value

        if verbose or (status_code >= 400 and status_code != 404):
            jsondata['ip'] = self.ip_address
            jsondata['lat'] = str(self.geo_lat)
            jsondata['long'] = str(self.geo_long)
            jsondata['city'] = str(self.geo_city)
            jsondata['cnty'] = str(self.geo_country)
            jsondata['host'] = str(self.http_host)
            jsondata['ua'] = str(self.http_user_agent)

        if (status_code <= 200 and settings.LOG_HTTP200) or (status_code == 404 and settings.LOG_HTTP404) or (status_code == 302 and settings.LOG_HTTP302):
            self.logger.info(msg=message, extra=jsondata)
        elif status_code == 400 and settings.LOG_HTTP400:
            self.logger.warning(msg=message, extra=jsondata)
        else:
            self.logger.critical(msg=message, extra=jsondata)

        def switch(x):
            return {
                200: message,
                302: message,
                400: SuspiciousOperation(message),
                403: SuspiciousOperation(message),
                404: Http404,
                422: SuspiciousOperation(message),
                500: HttpResponseServerError(message),
            }.get(x, 200)

        if status_code == 0:
            return
        else:
            return switch(status_code)

