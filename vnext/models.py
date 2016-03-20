from django.core.validators import URLValidator
from django.db import models as mydb


class LongURLs(mydb.Model):
    ORIGINALLY_ENCODED = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
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
    IS_ACTIVE = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
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
    ENTRY_TYPE = (
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
            choices=ENTRY_TYPE)
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


def __str__(self):
    return self.httpurl