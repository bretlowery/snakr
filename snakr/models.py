try:
    from dev_appserver_version import DEV_APPSERVER_VERSION
except ImportError:
    DEV_APPSERVER_VERSION = 2

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


def __str__(self):
    return self.httpurl