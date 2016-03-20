"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import django
from django.core.wsgi import get_wsgi_application
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secure.settings")

import snakr.loggr as loggr
event = loggr.SnakrEventLogger()
dt = datetime.datetime.now()
event.log(messagekey='STARTUP', dt=dt.isoformat())
event.log(messagekey='PYTHON_VERSION', value=sys.version)
event.log(messagekey='DJANGO_VERSION', value=django.get_version())

application = get_wsgi_application()
