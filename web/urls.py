from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from snakr.views import Dispatcher, maintenance_page
from django.http import HttpResponse

d = Dispatcher()
urlpatterns = [
        url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
#        url(r'^robots\.txt$', d.dispatch(
#                GET=d.robot_handler)),
        url(r'^.*', csrf_exempt(d.dispatch(
                GET=d.get_handler,
                POST=d.post_handler,
                ))),
        #url(r'^.*', maintenance_page),
]
