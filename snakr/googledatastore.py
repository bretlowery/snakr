from google.appengine.ext import ndb
import secure.settings as settings
import models
import loggr

class client():

    def __init__(self):
        self._event = loggr.SnakrEventLogger()

    def persist(self, **kwargs):
        if settings.DATASTORE_ENTITY:
            try:
                dad = models.EventStreamVersion.get_by_id(settings.SNAKR_VERSION, use_cache=False)
                if not dad:
                    dad = models.EventStreamVersion(id=settings.SNAKR_VERSION)
                    dad.event_stream_version = settings.SNAKR_VERSION
                    key = dad.put()
                else:
                    key = dad.key
                event = models.EventStream(parent=key)
                event.event_type = kwargs.pop("event_type", "Z")
                for e in settings.EVENT_TYPES:
                    if e[0] == event.event_type:
                        event.event_description = e[1]
                        break
                for e in settings.EVENT_STATUSES:
                    if e[0] == event.event_type:
                        event.event_status_code = e[1]
                        break
                event.http_status_code = int(kwargs.pop("http_status_code", -1))
                event.info = kwargs.pop("info", "none")
                event.longurl = kwargs.pop("longurl", "none")
                event.shorturl = kwargs.pop("shorturl", "none")
                event.ip = kwargs.pop("ip","::0")
                event.geo_latlong = ndb.GeoPt(float(kwargs.pop("geo_lat", 0.0)),float(kwargs.pop("geo_long", 0.0)))
                event.geo_city = kwargs.pop("geo_city", "none")
                event.geo_country = kwargs.pop("geo_country", "none")
                event.http_host = kwargs.pop("http_host", "none")
                event.http_useragent = kwargs.pop("http_useragent", "none")
                event.http_referer = kwargs.pop("http_referer", "none")
                event.developer_json = kwargs.pop("developer_json","{}")
                event.qa_json = kwargs.pop("qa_json", "{}")
                event.ops_json = kwargs.pop("ops_json", "{}")
                id = event.put()
                return id
            except Exception as e:
                raise self._event.log(messagekey='GOOGLEDATASTORE_ERROR', value=e.message, status_code=400)
        else:
            raise self._event.log(messagekey='GOOGLEDATASTORE_UNAVAILABLE', status_code=400)
