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

if not on_production_server:
    from django.db import models as mydb
else:
    from google.appengine.ext import ndb as mydb


class LongURLs(mydb.Model):
    ORIGINALLY_ENCODED = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    id = mydb.BigIntegerField(verbose_name='unique hash value of the long URL', primary_key=True, null=False)
    longurl = mydb.TextField(verbose_name='encoded, quoted version of the submitted long URL',
                              validators=[URLValidator()], null=False, blank=False)
    created_on = mydb.DateTimeField(verbose_name='datetime that the long URL was first submitted for shortening',
                                     auto_now=True)
    originally_encoded = mydb.CharField(verbose_name='Y=the long URL was encoded when submitted; N=otherwise',
                                         max_length=1, null=False, choices=ORIGINALLY_ENCODED)

    @classmethod
    def get(cls, id):
        return cls.get(id)

    class Meta:
        unique_together = ('longurl', 'id')


class ShortURLs(mydb.Model):
    IS_ACTIVE = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    id = mydb.BigIntegerField(verbose_name='unique hash value of the short URL', primary_key=True, null=False)
    longurl_id = mydb.OneToOneField(LongURLs,
                                     verbose_name='unique hash value of the long URL redirected to by the short URL',
                                     on_delete=mydb.CASCADE, unique=True, null=False)
    shorturl = mydb.CharField(verbose_name='unencoded, unquoted version of the short URL generated', max_length=32,
                               validators=[URLValidator()], null=False, blank=False)
    created_on = mydb.DateTimeField(verbose_name='datetime that the short URL was first generated', auto_now=True,
                                     null=False)
    is_active = mydb.CharField(
            verbose_name='Y=The short URL redirects to the long URL; N=The short URL generates a 404 error',
            max_length=1,
            null=False, choices=IS_ACTIVE)
    compression_ratio = mydb.DecimalField(verbose_name='ratio of compression achived long vs short', max_digits=10,
                                           decimal_places=2, null=False)

    @classmethod
    def get(cls, id):
        return cls.get(id)

    @classmethod
    def get_by_longurl_id(cls, longurl_id):
        return cls.get(longurl_id)

    class Meta:
        unique_together = (('longurl_id', 'id',), ('shorturl', 'id'), ('longurl_id', 'shorturl'))


class SnakrLog(mydb.Model):
    ENTRY_TYPE = (
        ('NL', 'New Long URL Submitted'),
        ('NS', 'New Short URL Created'),
        ('RS', 'Short URL Requested'),
        ('RL', 'Existing Long URL Resubmitted'),
    )
    log_order = mydb.AutoField(verbose_name='autoincrementing order of log events', primary_key=True, max_length=19,
                                null=False)
    logged_on = mydb.DateTimeField(verbose_name='datetime that the event was logged', auto_now=True, null=False)
    entry_type = mydb.CharField(
            verbose_name='NL=a new long URL was submitted, NS=a new short URL was created, RS=a short URL request was '
                         'made, RL=an existing long URL was resubmitted',
            max_length=2, null=False, choices=ENTRY_TYPE)
    longurl_id = mydb.BigIntegerField(verbose_name='unique hash value of the long URL', null=False)
    shorturl_id = mydb.BigIntegerField(verbose_name='unique hash value of the corresponding short URL', null=False)
    ip_address = mydb.CharField(verbose_name='IPv4 or IPv6 address of the origin of the request', max_length=45,
                                 null=False, blank=False)
    lat = mydb.DecimalField(verbose_name='latitude location of the origin of the request', max_digits=10,
                             decimal_places=8, null=False)
    long = mydb.DecimalField(verbose_name='longitude location of the origin of the request', max_digits=11,
                              decimal_places=8, null=False)

    @classmethod
    def get_by_shorturl_id(cls, shorturl_id, **kwargs):
        is_active = kwargs.get('is_active','Y')
        entry_type = kwargs.get('entry_type','')
        order_by = kwargs.get('order_by','')
        if order_by is not None:
            if is_active in ['Y', 'N']:
                if entry_type in ['NL', 'NS', 'RS', 'RL']:
                    return cls.query(shorturl_id).filter(is_active__exact=is_active).filter(
                            entry_type__exact=entry_type).order(order_by)
                else:
                    return cls.query(shorturl_id).filter(is_active__exact=is_active).order(order_by)
            else:
                if entry_type in ['NL', 'NS', 'RS', 'RL']:
                    return cls.query(shorturl_id).filter(entry_type__exact=entry_type).order(order_by)
                else:
                    return cls.query(shorturl_id).order(order_by)
        else:
            if is_active in ['Y', 'N']:
                if entry_type in ['NL', 'NS', 'RS', 'RL']:
                    return cls.query(shorturl_id).filter(is_active__exact=is_active).filter(
                            entry_type__exact=entry_type)
                else:
                    return cls.query(shorturl_id).filter(is_active__exact=is_active)
            else:
                if entry_type in ['NL', 'NS', 'RS', 'RL']:
                    return cls.query(shorturl_id).filter(entry_type__exact=entry_type)
                else:
                    return cls.query(shorturl_id)

    @classmethod
    def get_by_longurl_id(cls, longurl_id, is_active='Y', entry_type='', order_by=''):
        if order_by is not None:
            if is_active in ['Y', 'N']:
                if entry_type in ['NL', 'NS', 'RS', 'RL']:
                    return cls.query(longurl_id).filter(is_active__exact=is_active).filter(
                            entry_type__exact=entry_type).order(order_by)
                else:
                    return cls.query(longurl_id).filter(is_active__exact=is_active).order(order_by)
            else:
                if entry_type in ['NL', 'NS', 'RS', 'RL']:
                    return cls.query(longurl_id).filter(entry_type__exact=entry_type).order(order_by)
                else:
                    return cls.query(longurl_id).order(order_by)
        else:
            if is_active in ['Y', 'N']:
                if entry_type in ['NL', 'NS', 'RS', 'RL']:
                    return cls.query(longurl_id).filter(is_active__exact=is_active).filter(
                            entry_type__exact=entry_type)
                else:
                    return cls.query(longurl_id).filter(is_active__exact=is_active)
            else:
                if entry_type in ['NL', 'NS', 'RS', 'RL']:
                    return cls.query(longurl_id).filter(entry_type__exact=entry_type)
                else:
                    return cls.query(longurl_id)



def __str__(self):
    return self.httpurl
