from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from snakr.views import Dispatcher, maintenance_page
from django.http import HttpResponse
#from django.contrib import admin
#admin.autodiscover()

d = Dispatcher()
urlpatterns = [
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
    url(r'^.*', csrf_exempt(d.dispatch(
        GET=d.get_handler,
        POST=d.post_handler,
        ))),
]
