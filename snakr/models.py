from django.core.validators import URLValidator
from django.db import models as mydb
from google.appengine.ext import ndb
import secure.settings as settings

_EVENT_TYPE = settings.EVENT_TYPES

_YN = (
    ('Y', 'Yes'),
    ('N', 'No'),
)


class LongURLs(mydb.Model):
    ORIGINALLY_ENCODED = _YN
    id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the long URL',
            primary_key=True,
            null=False)
    longurl = mydb.CharField(
            verbose_name='encoded, quoted version of the submitted long URL',
            max_length=4096,
            validators=[URLValidator()],
            null=False,
            blank=False)
    created_on = mydb.DateTimeField(
            verbose_name='datetime that the long URL was first submitted for shortening',
            auto_now=True)
    originally_encoded = mydb.CharField(
            verbose_name='Y=the long URL was encoded when submitted; N=otherwise',
            max_length=1,
            null=False,
            choices=ORIGINALLY_ENCODED)

    class Meta:
        managed = False


class ShortURLs(mydb.Model):
    IS_ACTIVE = _YN
    id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the short URL',
            primary_key=True,
            null=False)
    longurl_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the long URL redirected to by the short URL',
            unique=True,
            null=False)
    shorturl = mydb.CharField(
            verbose_name='unencoded, unquoted version of the short URL generated',
            max_length=40,
            validators=[URLValidator()],
            null=False,
            blank=False)
    shorturl_path_size = mydb.SmallIntegerField(
            verbose_name='value of secure.SHORTURL_PATH_SIZE when short URL was generated',
            null=False)
    created_on = mydb.DateTimeField(
            verbose_name='datetime that the short URL was first generated',
            auto_now=True,
            null=False)
    is_active = mydb.CharField(
            verbose_name='Y=The short URL redirects to the long URL; N=The short URL generates a 404 error',
            max_length=1,
            null=False,
            choices=IS_ACTIVE)
    compression_ratio = mydb.DecimalField(
            verbose_name='ratio of compression achived long vs short',
            max_digits=10,
            decimal_places=2,
            null=False)

    class Meta:
        managed = False


class EventLog(mydb.Model):
    EVENT_TYPE = _EVENT_TYPE
    id = mydb.AutoField(
            verbose_name='unique 64-bit integer autoincrement; gives order of events (200s, 302s, 400s, 404s, 500s...) as they occurred',
            primary_key=True,
            null=False)
    logged_on = mydb.DateTimeField(
            verbose_name='datetime that the event was inserted into the table',
            auto_now=True)
    event_type = mydb.CharField(
            verbose_name='Type of event logged. See models.Events.ENTRY_TYPE for enumeration details.',
            max_length=1,
            null=False,
            choices=EVENT_TYPE)
    http_status_code = mydb.IntegerField(
            verbose_name='the HTTP status code, if any, on the event, e.g. 200, 302, 404, etc.',
            null = False)
    message = mydb.CharField(
            verbose_name='Human-readable text message about the event, if any.',
            max_length=8192,
            null=False)
    longurl_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the long URL redirected to by the short URL associated with the event, if any',
            null=False)
    shorturl_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the short URL associated with the event, if any',
            null=False)
    ip_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the IP address origin of the event, if any',
            null=False)
    lat = mydb.DecimalField(
            verbose_name='Latitude coordinate of the origin of the event, if any',
            max_digits = 10,
            decimal_places= 8,
            null = False)
    lng = mydb.DecimalField(
            verbose_name='Longitude coordinate of the origin of the event, if any',
            max_digits = 11,
            decimal_places= 8,
            null = False)
    city_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the city of origin of the event, if any',
            null=False)
    country_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the country of origin of the event, if any',
            null=False)
    host_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the HTPP_HOST value in the event, if any',
            null=False)
    useragent_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the HTPP_USER_AGENT value in the event, if any',
            null=False)
    referer = mydb.CharField(
            verbose_name='the HTTP_REFERER from which this event was received',
            max_length=2083,
            null=False)
    snakr_version = mydb.CharField(
            verbose_name='the Snakr version/build number at the time of the event',
            max_length=40,
            null=False)

    class Meta:
        managed = False


class UserAgentLog(mydb.Model):
    id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the HTPP_USER_AGENT value in the event, if any',
            primary_key=True,
            null=False)
    useragent = mydb.CharField(
            verbose_name='The HTTP_USER_AGENT value in the event, if any.',
            max_length=8192,
            null=False)
    is_blacklisted = mydb.CharField(
            verbose_name='If Y, 403 any request received containing this value.',
            max_length=1,
            default='N',
            null=False)

    class Meta:
        managed = False


class HostLog(mydb.Model):
    id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the HTPP_HOST value in the event, if any',
            primary_key=True,
            null=False)
    host = mydb.CharField(
            verbose_name='The HTTP_HOST value in the event, if any.',
            max_length=253,
            null=False)
    is_blacklisted = mydb.CharField(
            verbose_name='If Y, 403 any request received containing this value.',
            max_length=1,
            default='N',
            null=False)

    class Meta:
        managed = False


class CityLog(mydb.Model):
    id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the city of origin of the event, if any',
            primary_key=True,
            null=False)
    city = mydb.CharField(
            verbose_name='The city of origin of the event, if any.',
            max_length=100,
            null=False)
    is_blacklisted = mydb.CharField(
            verbose_name='If Y, 403 any request received containing this value.',
            max_length=1,
            default='N',
            null=False)

    class Meta:
        managed = False


class CountryLog(mydb.Model):
    id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the country of origin of the event, if any',
            primary_key=True,
            null=False)
    country = mydb.CharField(
            verbose_name='The country of origin of the event, if any.',
            max_length=100,
            null=False)
    is_blacklisted = mydb.CharField(
            verbose_name='If Y, 403 any request received containing this value.',
            max_length=1,
            default='N',
            null=False)

    class Meta:
        managed = False


class IPLog(mydb.Model):
    id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the IPv4 or IPv6 of the event, if any',
            primary_key=True,
            null=False)
    ip = mydb.CharField(
            verbose_name='The IPv4 or IPv6 address of the event, if any.',
            max_length=45,
            null=False)
    is_blacklisted = mydb.CharField(
            verbose_name='If Y, 403 any request received containing this value.',
            max_length=1,
            default='N',
            null=False)

    class Meta:
        managed = False


#Third Party IP Blacklists
class TPIpBls(mydb.Model):
    id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the blacklist name (the 1st value) in each entry in settings.THRIDPARTY_BLACKLISTS',
            primary_key=True,
            null=False)
    name = mydb.CharField(
            verbose_name='each blacklist name (the 1st value) in each entry in settings.THRIDPARTY_BLACKLISTS',
            max_length=100,
            null=False)
    download_from_url = mydb.CharField(
            verbose_name='URL location of the remote source of the blacklist',
            max_length=4096,
            validators=[URLValidator()],
            null=False,
            blank=False)
    first_loaded_on = mydb.DateTimeField(
            verbose_name='datetime that the blacklist was first successfully loaded from the remote source',
            null=True)
    last_loaded_on = mydb.DateTimeField(
            verbose_name='datetime that the blacklist was last successfully loaded from the remote source',
            null=True)

    class Meta:
        managed = False


#Third Party IP Blacklist Ranges
class TPIpBl_Ranges(mydb.Model):
    id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the blacklist name (the 1st value) in each entry in settings.THRIDPARTY_BLACKLISTS',
            primary_key=True,
            null=False)
    ip_range = mydb.CharField(
            verbose_name='One or more IPv4 entries in the 3rd party blacklist; formats a.b.c.d, a.b.c.d/nn, or a.b.c.d-w.x.y.z',
            primary_key=True,
            max_length=50,
            null=False,
            blank=False)
    class Meta:
        managed = False


class EventStreamVersion(ndb.Model):
    event_stream_version = ndb.StringProperty(indexed=True)

    class Meta:
        managed = False


class EventStream(ndb.Model):
    event_version = ndb.StringProperty(indexed=True)
    logged_on = ndb.DateTimeProperty(indexed=True, auto_now_add=True)
    event_type = ndb.StringProperty(indexed=True)
    event_description = ndb.StringProperty(indexed=False)
    event_status_code = ndb.IntegerProperty(indexed=True)
    http_status_code = ndb.IntegerProperty(indexed=True)
    info = ndb.StringProperty(indexed=False)
    longurl = ndb.StringProperty(indexed=False)
    # longurl_lower = ndb.ComputedProperty(lambda self: self.longurl.lower())
    shorturl = ndb.StringProperty(indexed=False)
    # shorturl_lower = ndb.ComputedProperty(lambda self: self.shorturl.lower())
    ip_address = ndb.StringProperty(indexed=True)
    # ip_address_lower = ndb.ComputedProperty(lambda self: self.ip_address.lower())
    geo_latlong = ndb.GeoPtProperty(indexed=False)
    geo_city = ndb.StringProperty(indexed=True)
    geo_city_lower = ndb.ComputedProperty(lambda self: self.geo_city.lower())
    geo_country = ndb.StringProperty(indexed=True)
    geo_country_lower = ndb.ComputedProperty(lambda self: self.geo_country.lower())
    http_host = ndb.StringProperty(indexed=True)
    http_host_lower = ndb.ComputedProperty(lambda self: self.http_host.lower())
    http_useragent = ndb.StringProperty(indexed=False)
    http_useragent_lower = ndb.ComputedProperty(lambda self: self.http_useragent.lower())
    json_annotation = ndb.StringProperty(indexed=False)

    class Meta:
        managed = False

    @classmethod
    def query_event_by_id(cls, id):
        return cls.get_by_id(id)

    @classmethod
    def query_event_by_type(cls, event_type):
        return cls.query(event_type=event_type).order(-cls.logged_on)

    @classmethod
    def query_event_by_http_status_code(cls, http_status_code, order_by_date=True):
        if order_by_date:
            return cls.query(http_status_code=http_status_code).order(-cls.logged_on, cls.event_type, cls.ip_address)
        else:
            return cls.query(http_status_code=http_status_code).order(cls.event_type, cls.ip_address)

    @classmethod
    def query_event_by_ip(cls, ip, order_by_date=True):
        if order_by_date:
            return cls.query(ip=ip).order(-cls.logged_on, cls.event_type, cls.ip_address)
        else:
            return cls.query(ip=ip).order(cls.event_type, cls.ip_address)

    @classmethod
    def query_event_by_country_and_city(cls, country, city, order_by_date=True):
        if order_by_date:
            return cls.query(country=country, city=city).order(-cls.logged_on, cls.event_type, cls.ip_address)
        else:
            return cls.query(country=country, city=city).order(cls.event_type, cls.ip_address)

    @classmethod
    def query_event_by_http_host(cls, http_host, order_by_date=True):
        if order_by_date:
            return cls.query(http_host=http_host).order(-cls.logged_on, cls.event_type, cls.ip_address)
        else:
            return cls.query(http_host=http_host).order(cls.event_type, cls.ip_address)

    @classmethod
    def query_event_by_http_useragent_hash(cls, http_useragent_hash, order_by_date=True):
        if order_by_date:
            return cls.query(http_useragent_hash=http_useragent_hash).order(-cls.logged_on, cls.event_type, cls.ip_address)
        else:
            return cls.query(http_useragent_hash=http_useragent_hash).order(cls.event_type, cls.ip_address)

def __str__(self):
    return self.httpurl
