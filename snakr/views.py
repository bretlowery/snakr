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

from shorturls import ShortURL
from longurls import LongURL

def dispatcher(**table):

    def invalid_method(request, *args, **kwargs):
        r = request.method
        return HttpResponseNotAllowed(r)

    def d(request, *args, **kwargs):
        h = table.get(request.method, invalid_method)
        return h(request, *args, **kwargs)

    return d


def get_handler(request, *args, **kwargs):
    s = ShortURL()
    return gello(request, 'GET', s.normalized_shorturl)


def post_handler(request, *args, **kwargs):
    l = LongURL(request)
    shorturl = l.persist(request)
    return HttpResponse(shorturl)


def gello(request, *args, **kwargs):
    now = datetime.datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')
    return HttpResponse("response.html",{"pn":"snakrv2.01" , "dt":now, "rm":args[0], "url":args[1]})

