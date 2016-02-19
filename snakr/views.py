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

import datetime
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse
import json
from shorturls import ShortURL
from longurls import LongURL
from django.http import Http404

def dispatcher(**table):

    def invalid_method(request, *args, **kwargs):
        r = request.method
        return HttpResponseNotAllowed(r)

    def d(request, *args, **kwargs):
        h = table.get(request.method, invalid_method)
        return h(request, *args, **kwargs)

    return d


def get_handler(request, *args, **kwargs):
    # create an instance of the ShortURL object, validate the short URL, and if successful load the ShortURL instance with it
    s = ShortURL()
    # lookup the long url previously used to generate the short url
    longurl = s.getlongurl(request)
    # if found, 302 to it; otherwise, 404
    if longurl:
        return HttpResponseRedirect(longurl)
    else:
        return Http404


def post_handler(request, *args, **kwargs):
    # create an instance of the LongURL object, validate the long URL, and if successful load the LongURL instance with it
    l = LongURL(request)
    # generate the shorturl and either persist both the long and short urls if new,
    # or lookup the matching short url if it already exists (i.e. the long url was submitted a 2nd or subsequent time)
    shorturl = l.get_or_make_shorturl(request)
    # return the shorturl as JSON
    response_data = {}
    response_data['shorturl'] = shorturl
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# def hello(request, *args, **kwargs):
#     now = datetime.datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')
#     return HttpResponse("response.html",{"pn":"snakrv2.01" , "dt":now, "rm":args[0], "url":args[1]})

