# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import bug workaround: http://stackoverflow.com/questions/32761566/django-1-9-importerror-for-import-module
# from djangoappengine.settings_base import *

import ipaddr
import os

try:
    from dev_appserver_version import DEV_APPSERVER_VERSION
except ImportError:
    DEV_APPSERVER_VERSION = 2

# Initialize App Engine SDK if necessary.
# try:
#     from google.appengine.api import apiproxy_stub_map
# except ImportError:
#     from djangoappengine.boot import setup_env
#     setup_env(DEV_APPSERVER_VERSION)

# from djangoappengine.utils import on_production_server
from django.core.validators import URLValidator

# if not on_production_server:
#    from django.db import models as mydb
# else:
#    from google.appengine.ext import ndb as mydb

from django.db import models as mydb
from utils import utils


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


class Log(mydb.Model):
    ENTRY_TYPE = (
        ('L', 'New Long URL Submitted'),
        ('S', 'Short URL Requested'),
        ('R', 'Existing Long URL Resubmitted'),
    )
    log_order = mydb.AutoField(
            verbose_name='autoincrementing order of log events',
            primary_key=True,
            max_length=20,
            null=False)
    logged_on = mydb.DateTimeField(
            verbose_name='datetime that the event was logged',
            auto_now=True,
            null=False)
    entry_type = mydb.CharField(
            verbose_name='L=a new long URL POST was submitted, S=a short URL GET request was made, R=an existing long '
                         'URL was resubmitted',
            max_length=1,
            null=False,
            choices=ENTRY_TYPE)
    longurl_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the long URL',
            null=False)
    shorturl_id = mydb.BigIntegerField(
            verbose_name='unique 64-bit integer binary hash value of the corresponding short URL',
            null=False)
    cli_ip_address = mydb.BinaryField(
            verbose_name='128-bit binary representation of the IPv4 or IPv6 address of the origin of the request',
            max_length=128,
            null=False,
            blank=False)
    cli_geo_lat = mydb.DecimalField(
            verbose_name='latitude location of the origin of the request',
            max_digits=10,
            decimal_places=8,
            null=False)
    cli_geo_long = mydb.DecimalField(
            verbose_name='longitude location of the origin of the request',
            max_digits=11,
            decimal_places=8,
            null=False)
    cli_geo_city = mydb.CharField(
            verbose_name='city of the origin of the request',
            max_length=100,
            null=False,
            blank=False)
    cli_geo_country = mydb.CharField(
            verbose_name='country of the origin of the request',
            max_length=100,
            null=False,
            blank=False)
    cli_http_host = mydb.CharField(
            verbose_name='HTTP_HOST value from the client',
            max_length=253,
            null=False,
            blank=False)
    cli_http_user_agent_id = mydb.BigIntegerField(
            verbose_name='64-bit integer binary hash value of the user agent',
            null=False)


class UserAgents(mydb.Model):
    id = mydb.BigIntegerField(
            verbose_name='64-bit integer binary hash value of the user agent',
            primary_key=True,
            null=False)
    cli_http_user_agent = mydb.CharField(
            verbose_name='USER_AGENT of the client',
            max_length=8192,
            null=False,
            blank=False)


def get_clientinfo(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
         readable_ip_address = x_forwarded_for.split(',')[0]
    else:
        readable_ip_address = request.META.get('REMOTE_ADDR', 'unknown')
    if readable_ip_address == 'unknown':
        binary_ip_address = bin(0)
    else:
        try:
            binary_ip_address = bin(ipaddr.IP(readable_ip_address).broadcast)[2:]
        except:
            binary_ip_address = bin(0)
            pass
    slatlong = request.META.get('HTTP_X_APPENGINE_CITYLATLONG', '0.0,0.0')
    geo_lat = slatlong.split(',')[0]
    geo_long = slatlong.split(',')[1]
    geo_city = request.META.get('HTTP_X_APPENGINE_CITY', 'unknown')
    geo_country = request.META.get('HTTP_X_APPENGINE_COUNTRY','unknown')
    http_host = request.META.get('HTTP_HOST','unknown')
    http_user_agent = request.META.get('HTTP_USER_AGENT','unknown')
    return binary_ip_address, geo_lat, geo_long, geo_city, geo_country, http_host, http_user_agent


def writelog(request, entry_type, longurl_id, shorturl_id, **kwargs):

    binary_ip_address, geo_lat, geo_long, geo_city, geo_country, http_host, http_user_agent = get_clientinfo(request)

    http_user_agent_id = utils.get_hash(http_user_agent)
    ua_found = True
    try:
        ua = UserAgents.objects.get(id = http_user_agent_id)
    except:
        ua_found = False
        pass
    if not ua_found:
        ua = UserAgents(id = http_user_agent_id, cli_http_user_agent = http_user_agent)

    l = Log(entry_type=entry_type,
            longurl_id=longurl_id,
            shorturl_id=shorturl_id,
            cli_ip_address=binary_ip_address,
            cli_geo_lat=geo_lat,
            cli_geo_long=geo_long,
            cli_geo_city=geo_city,
            cli_geo_country=geo_country,
            cli_http_host=http_host,
            cli_http_user_agent_id=http_user_agent_id)
    l.save()

    return


def __str__(self):
    return self.httpurl