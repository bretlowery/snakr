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

import json
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, Http404
from shorturls import ShortURL
from longurls import LongURL
from urlparse import urlparse, parse_qs
import webapp2
import secure.settings as settings
from PyOpenGraph import PyOpenGraph
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup
# from django.views.generic import TemplateView
from django.shortcuts import render_to_response
import logger


def maintenance_page(self, request):
    return HttpResponse("<H1>The system is down for maintenance.</H1>", content_type="text/html")


class Dispatcher(webapp2.RequestHandler):

    def __init__(self):
        return

    def dispatch(self, **table):

        def invalid_method(request, *args, **kwargs):
            r = request.method
            return HttpResponseNotAllowed(r)

        def d(request, *args, **kwargs):
            h = table.get(request.method, invalid_method)
            return h(request, *args, **kwargs)

        return d


    def robot_handler(self, request, *args, **kwargs):
        log = logger.Loggr(request)
        log.event(messagekey='ROBOT', verbose=True, status_code=200)
        return lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")


    def get_handler(self, request, *args, **kwargs):
        #
        # check to see if a long url was submitted for shortening via a query parameter
        #
        url_parts = urlparse(request.build_absolute_uri())
        if url_parts.query:
            qsurl = parse_qs(urlparse(request.build_absolute_uri()))["u"]
            if qsurl:
                return self.post_handler(request)
        #
        # create an instance of the ShortURL object, validate the short URL, and if successful load the ShortURL instance with it
        #
        s = ShortURL(request)
        #
        # lookup the long url previously used to generate the short url
        #
        longurl = s.getlongurl(request)
        #
        # if found, 302 to it; otherwise, 404
        #
        if longurl:
            return HttpResponseRedirect(longurl)
        else:
            return Http404

    def post_handler(self, request, *args, **kwargs):
        #
        # Restrict new short url creation to GAE project owners
        # Outside offworlders will get a 404 on POST
        #
        # user = users.get_current_user()
        # # raise SuspiciousOperation(str(user))
        # if user:
        #     if not users.is_current_user_admin():
        #         raise Http404
        # else:
        #     raise Http404
        #
        # create an instance of the LongURL object, validate the long URL, and if successful load the LongURL instance with it
        #
        l = LongURL(request)
        #
        # generate the shorturl and either persist both the long and short urls if new,
        # or lookup the matching short url if it already exists (i.e. the long url was submitted a 2nd or subsequent time)
        #
        shorturl = l.get_or_make_shorturl(request)
        #
        # prepare to return the shorturl as JSON
        #
        response_data = {}
        #
        # if settings.OGTITLE = True, get the OpenGraph title meta tag value and include it in the output
        # see: http://ogp.me
        # for the Python PyOpenGraph site: https://pypi.python.org/pypi/PyOpenGraph
        #
        title_exists = False
        try:
            title = PyOpenGraph.PyOpenGraph(l.longurl)
            title_exists = title.is_valid()
        except UnicodeDecodeError:
            pass
        if title_exists:
            title = title.metadata['title'].decode('utf-8')
        else:
            try:
                longurl_page = urlfetch.fetch(l.normalized_longurl)
                longurl_html = BeautifulSoup(longurl_page)
                title = longurl_html.title.decode('utf-8').string
            except:
                title = ''
                pass
        #
        # return meta tag values as well if requested
        #
        if settings.RETURN_ALL_META:
            j = json.JSONEncoder()
            for key, value in request.META.items():
                if isinstance(key, (list, dict, str, unicode, int, float, bool, type(None))):
                    try:
                        response_data[key] = j.encode(value)
                    except:
                        response_data[key] = 'nonserializable'
        #
        # return JSON to caller
        #
        response_data['shorturl'] = shorturl
        if title_exists:
            ls = len(shorturl)
            lt = len(title)
            ltmax = 140 - ls - 1
            if lt > ltmax:
                tweet = title[:ltmax-3]+'... '+shorturl
            else:
                tweet = title + ' ' + shorturl
            response_data['twitterfriendly'] = tweet
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def test_post_handler(self, request, *args, **kwargs):
        return HttpResponse("<H2>Test value: {%s}</H2>", content_type="text/html")

