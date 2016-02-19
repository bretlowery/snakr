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
from djangoappengine.settings_base import *

try:
    from dev_appserver_version import DEV_APPSERVER_VERSION
except ImportError:
    DEV_APPSERVER_VERSION = 2

# Initialize App Engine SDK if necessary.
try:
    from google.appengine.api import apiproxy_stub_map
except ImportError:
    from djangoappengine.boot import setup_env
    setup_env(DEV_APPSERVER_VERSION)

from djangoappengine.utils import on_production_server
from django.core.validators import URLValidator

#if not on_production_server:
#    from django.db import models as mydb
#else:
#    from google.appengine.ext import ndb as mydb

from django.db import models as mydb
from utils import utils

class LongURLs(mydb.Model):
    ORIGINALLY_ENCODED = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    id = mydb.BigIntegerField(verbose_name='unique SHA1 binary hash value of the long URL', primary_key=True, null=False)
    longurl = mydb.CharField(verbose_name='encoded, quoted version of the submitted long URL',
                              max_length=4096, validators=[URLValidator()], null=False, blank=False)
    created_on = mydb.DateTimeField(verbose_name='datetime that the long URL was first submitted for shortening',
                                     auto_now=True)
    originally_encoded = mydb.CharField(verbose_name='Y=the long URL was encoded when submitted; N=otherwise',
                                         max_length=1, null=False, choices=ORIGINALLY_ENCODED)


class ShortURLs(mydb.Model):
    IS_ACTIVE = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    id = mydb.BigIntegerField(verbose_name='unique SHA1 binary hash value of the short URL', primary_key=True, null=False)
    longurl_id = mydb.BigIntegerField(verbose_name='unique SHA1 binary hash value of the long URL redirected to by the short URL',
                                     unique=True, null=False)
    shorturl = mydb.CharField(verbose_name='unencoded, unquoted version of the short URL generated', max_length=40,
                               validators=[URLValidator()], null=False, blank=False)
    shorturl_path_size = mydb.SmallIntegerField(verbose_name='value of settings.SHORTURL_PATH_SIZE when short URL was generated',
                               null=False)
    created_on = mydb.DateTimeField(verbose_name='datetime that the short URL was first generated', auto_now=True,
                                     null=False)
    is_active = mydb.CharField(
            verbose_name='Y=The short URL redirects to the long URL; N=The short URL generates a 404 error',
            max_length=1,
            null=False, choices=IS_ACTIVE)
    compression_ratio = mydb.DecimalField(verbose_name='ratio of compression achived long vs short', max_digits=10,
                                           decimal_places=2, null=False)


class Log(mydb.Model):
    ENTRY_TYPE = (
        ('L', 'New Long URL Submitted'),
        ('S', 'New Short URL Created'),
        ('R', 'Short URL Requested'),
        ('X', 'Existing Long URL Resubmitted'),
    )
    log_order = mydb.AutoField(verbose_name='autoincrementing order of log events', primary_key=True, max_length=19,
                                null=False)
    logged_on = mydb.DateTimeField(verbose_name='datetime that the event was logged', auto_now=True, null=False)
    entry_type = mydb.CharField(
            verbose_name='NL=a new long URL was submitted, NS=a new short URL was created, RS=a short URL request was '
                         'made, RL=an existing long URL was resubmitted',
            max_length=1, null=False, choices=ENTRY_TYPE)
    longurl_id = mydb.BigIntegerField(verbose_name='unique SHA1 binary hash value of the long URL', null=False)
    shorturl_id = mydb.BigIntegerField(verbose_name='unique SHA1 binary hash value of the corresponding short URL', null=False)
    ip_address = mydb.CharField(verbose_name='IPv4 or IPv6 address of the origin of the request', max_length=45,
                                 null=False, blank=False)
    lat = mydb.DecimalField(verbose_name='latitude location of the origin of the request', max_digits=10,
                             decimal_places=8, null=False)
    long = mydb.DecimalField(verbose_name='longitude location of the origin of the request', max_digits=11,
                              decimal_places=8, null=False)
    city_of_origin = mydb.CharField(verbose_name='city of the origin of the request', max_length=100, null=False, blank=False)
    country_of_origin = mydb.CharField(verbose_name='country of the origin of the request', max_length=100, null=False, blank=False)


def savelog(request, entry_type, longurl_id, shorturl_id):
    ip_address, lat, lng, city, country = utils.get_demographics(request)
    l = Log(entry_type=entry_type, longurl_id=longurl_id, shorturl_id=shorturl_id,
            ip_address=ip_address, lat=lat, long=lng, city_of_origin=city, country_of_origin=country)
    l.save()
    return

def __str__(self):
    return self.httpurl

