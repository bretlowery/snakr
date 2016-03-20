
from patterns.singleton import Singleton

class gaeinit():

    def __init__(self):
        # Initialize Google App Engine SDK if necessary.
        # This is required when debugging in command-line Python
        #
        # there can be only one
        # see Method 3 on http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
        #
        __metaclass__ = Singleton
        #
        #
        #
        try:
            from dev_appserver_version import DEV_APPSERVER_VERSION
        except ImportError:
            DEV_APPSERVER_VERSION = 2
        try:
            from google.appengine.api import urlfetch
        except ImportError:
            from djangoappengine.boot import setup_env
            setup_env(DEV_APPSERVER_VERSION)
            from google.appengine.api import urlfetch
            from google.appengine.api import apiproxy_stub_map, urlfetch_stub
            apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
            apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())


