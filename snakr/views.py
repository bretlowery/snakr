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

import textwrap
import datetime
#from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseNotAllowed

from get_shorturl import GetShortURL


def dispatcher(**table):

    def invalid_method(request, *args, **kwargs):
        r = request.method
        return HttpResponseNotAllowed(r)

    def d(request, *args, **kwargs):
        h = table.get(request.method, invalid_method)
        return h(request, *args, **kwargs)

    return d


def get_handler(request, *args, **kwargs):
    g = GetShortURL(request)
    return hello()


def post_handler(self, *args, **kwargs):
    return None


def hello(*args, **kwargs):
    now = datetime.datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')
    response_text = textwrap.dedent('''\
            <html>
            <head>
                <title>snakrv2.001</title>
            </head>
            <body>
                <h1>The Current Time Here Is:</h1>
                <p>%s</p>
            </body>
            </html>
        ''' % now)
    return HttpResponse(response_text)

