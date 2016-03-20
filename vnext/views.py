import json
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, Http404
from shorturls import ShortURL
from longurls import LongURL
from urlparse import urlparse
import webapp2
import secure.settings as settings
import parsers
from botprotection import BotDetector

def maintenance_page(self, request):
    return HttpResponse("<H1>The system is down for maintenance.</H1>", content_type="text/html")


class Dispatcher(webapp2.RequestHandler):

    def __init__(self):
        super(Dispatcher, self).__init__()
        self._botdetector = BotDetector()
        return

    def dispatch(self, **table):

        def invalid_method(request, *args, **kwargs):
            r = request.method
            return HttpResponseNotAllowed(r)

        def d(request, *args, **kwargs):
            h = table.get(request.method, invalid_method)
            return h(request, *args, **kwargs)

        return d

    def get_handler(self, request, *args, **kwargs):
        #
        # check for unfriendly bot first
        #
        self._botdetector.if_bot_then_403(request)
        #
        # check to see if a long url was submitted for shortening via the "u" query parameter
        #
        url_parts = urlparse(request.build_absolute_uri())
        #
        # if not, create an instance of the ShortURL object, validate the short URL,
        # #and if successful load the ShortURL instance with it
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
        # check for unfriendly bot first
        #
        self._botdetector.if_bot_then_403(request)
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
        # get document title if possible
        #
        p = parsers.Parsers()
        title = p.get_title(l.longurl)
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
        if title:
            ls = len(shorturl)
            lt = len(title)
            ltmax = 140 - ls - 1
            if lt > ltmax:
                socialmediapost = title[:ltmax-3]+'... '+shorturl
            else:
                socialmediapost = title + ' ' + shorturl
            response_data['socialmediapost'] = socialmediapost
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def test_post_handler(self, request, *args, **kwargs):
        return HttpResponse("<H2>Test value: {%s}</H2>", content_type="text/html")

