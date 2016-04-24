"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
#
# NOTE: changing the ordering of most anything in wsgi.py will most likely break something somewhere
# Be very careful when deploying changes
#
#
# required pre-Django init
#
import os
import sys
os.environ.setdefault("SNAKR_GAE_HOST", "snakrv2.appspot.com")
os.environ.setdefault("SNAKR_ROOT_URLCONF", "snakr.urls")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secure.settings")
#
# Django init
#
import django
django.setup()
#
# post-Djngo init
#
from django.core.wsgi import get_wsgi_application
import datetime
import loggr as loggr
event = loggr.SnakrEventLogger()
import secure.settings as settings

dt = datetime.datetime.now()
event.log(messagekey='STARTUP', dt=dt.isoformat(), value=settings.SNAKR_VERSION)
event.log(messagekey='PYTHON_VERSION', value=sys.version)
event.log(messagekey='DJANGO_VERSION', value=django.get_version())
application = get_wsgi_application()
