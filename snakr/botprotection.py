from patterns.singleton import Singleton
from secure.gae import gaeinit
gaeinit()
import loggr
from utilities import Utils

class BotDetector():

    def __init__(self, *args, **kwargs):
        #
        # there can be only one
        # see Method 3 on http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
        #
        __metaclass__ = Singleton
        #
        self._event = loggr.SnakrEventLogger()
        self._event.log(event_type='I', message='Loading botdetector')
        #
        # known bot list
        # all entries must be lowercase
        #
        self._known_bots = ['1job', 'abot', 'agentname', 'apachebench', 'aport', 'applesyndication', 'ask jeeves', 'ask+jeeves',
                            'atomz', 'avantgo', 'baiduspider', 'blitzbot', 'bloglines', 'bordermanager', 'changedetection',
                            'check_http', 'checkurl', 'chkd', 'contype', 'cosmos', 'download ninja', 'download+ninja', 'dts agent',
                            'dts+agent', 'favorg', 'flashget', 'frontier', 'getright', 'golem', 'gomezagent', 'googlebot', 'grabber',
                            'hitlist', 'ia_archive', 'ibot', 'ichiro', 'ieautodiscovery', 'indy library', 'indy+library', 'infolink',
                            'internet ninja', 'internet+ninja', 'internetseer', 'isilo', 'jakarta', 'jobo', 'justview', 'keynote', 'kinja',
                            'larbin', 'libwww-perl', 'linkbot', 'linkchecker', 'linklint', 'linkscan', 'linkwalker', 'lisa', 'lwp', 'lydia',
                            'magus bot', 'magus+bot', 'mediapartners-google', 'mfc_tear_sample',
                            'microsoft scheduled cache content download service', 'microsoft url control',
                            'microsoft+scheduled+cache+content+download+service', 'microsoft+url+control', 'miva', 'mj12bot', 'monitor',
                            'monster', 'mozilla/5.0 (compatible; msie 5.0)', 'mozilla/5.0+(compatible;+msie+5.0)', 'ms frontpage',
                            'ms search', 'ms+frontpage', 'ms+search', 'msnptc', 'nbot', 'newsnow', 'nextgensearchbot', 'nomad', 'npbot',
                            'nutch', 'nutscrape', 'omniexplorer', 'patric', 'pioneer', 'pluck', 'plumtree', 'powermarks', 'psbot', 'rpt-http',
                            'rssreader', 'scooter', 'seekbot', 'sherlock', 'shopwiki', 'slurp', 'stackrambler', 'sucker', 'templeton', '/teoma',
                            'thunderstone', 't-h-u-n-d-e-r-s-t-o-n-e', 'topix', 'ukonline', 'ultraseek', 'urchin', 'vagabondo', 'voyager',
                            'web downloader', 'web+downloader', 'webauto', 'webcapture', 'webcheck', 'webcopier', 'webdup', 'webtool', 'wfarc',
                            'wget', 'whatsup', 'xenu', 'yacy', 'zealbot', 'zeus', 'ez publish link validator', 'ez+publish+link+validator',
                            'terrawizbot', 'goldfire', 'sitevigil', 'iopus', 'microsoft bits', 'microsoft+bits', 'heritrix', 'yahoofeedseeker',
                            'internal zero-knowledge agent', 'internal+zero-knowledge+agent', 'surveybot/', 'liferea', 'yahooseeker', 'findlinks',
                            'oodlebot', 'adsbot-google', 'innovantagebot', 'khte', 'ktxn', 'advanced email extractor', 'advanced+email+extractor',
                            'moreoverbot', 'webbot', 'search_comments\\at\\sensis\\dot\\com\\dot\\au', 'panscient.com', 'snoopy', 'bot/1.0',
                            'universalsearch', 'maxamine', 'argus', 'google wireless transcoder', 'google+wireless+transcoder', 'clickajob',
                            'jobrapido', 'python-urllib', 'isearch', 'http://bot.ims.ca', 'system center operations manager',
                            'system+center+operations+manager', 'joedog', 'websitepulse', 'bitvouseragent',
                            'mozilla/4.0 (compatible; msie 6.0; windows nt 5.1;1813)',
                            'mozilla/4.0+(compatible;+msie+6.0;+windows+nt+5.1;1813)',
                            'paros', 'watchmouse', 'proximic', 'scoutjet', 'twiceler', 'pingdom', 'europarchive', 'search-engine-studio',
                            'webmetrics', 'holmes', 'alertsite', 'yahoo pipes', 'yahoo+pipes', 'simplepie', 'drupal', 'htmlparser',
                            'watchfire webxm', 'watchfire+webxm', 'snappreviewbot', 'snapbot', 'daumoa', 'nielsen adr', 'nielsen+adr',
                            'evrinid', 'fdm 3.x', 'fdm+3.x', 'isense bot', 'isense+bot', 'trovit', 'riverglassscanner', 'wepbot', 'mlbot',
                            'siteimprove', 'archive.org', 'vocusbot', 'fairshare', 'blp_bbot', 'w3c_validator',
                            '(simulated_by_webserver_stress_tool)', 'wapt', 'updatepatrol', 'sitecon', 'twitterbot', 'bingbot', 'www-mechanize',
                            'google web preview', 'google+web+preview', 'adgbot', 'httpunit', 'curious george', 'curious+george', 'postrank',
                            'httpcomponents', 'twisted pagegetter', 'twisted+pagegetter', 'servers alive url check', 'servers+alive+url+check',
                            'appengine-google', 'yioopbot', 'flamingo_searchengine', 'atomic_email_hunter', 'feedburner', 'talktalk',
                            'facebookexternalhit', 'adbeat', 'sjn', 'outbrain', 'tweetmemebot', 'wasalive', 'wikiwix-bot', 'ezooms', 'hiscan',
                            'd24y-aegis', 'google-hoteladsverifier', 'fupbot', 'moatbot', 'vmcbot', 'wusage/', 'wikiofeedbot', 'jobblebot',
                            'companydatatree', 'cookiereports', 'wbsearchbot', 'bingpreview', 'scan', 'smokeping', 'flamingosearch', 'reconnoiter',
                            'ec2linkfinder', 'citeseerxbot', 'funnelback', 'feed43', 'auditbot', 'genieo', 'nerdbynature', 'python-httplib',
                            'cutbot', 'server density external llama', 'server+density+external+llama', 'mna digital circonus check',
                            'mna+digital+circonus+check', 'aware', 'appneta sequencer', 'appneta+sequencer', 'scanalert', 'catchpoint',
                            'discoverybot', 'jooblebot', 'bitlybot', 'adr)', 'yottaamonitor', 'adometrybot', 'tsmbot', 'orangebot-mobile',
                            'phantomjs', 'scc internet services - url check', 'scc+internet+services+-+url+check',
                            'apache-httpclient/4.1.1 (java 1.5)', 'apache-httpclient/4.1.1+(java+1.5)', 'tagscanner', 'loadimpactpageanalyzer',
                            'cfschedule', 'searchme.com/support/', 'b2w', 'coast', 'combine', 'crawl', 'crescent', 'curl', 'dialer', 'echo',
                            'fetch', 'grub', 'harvest', 'httrack', 'newsapp', 'ng/2.0', 'obot', 'pita', 'sohu', 'spider', 'spike', 'stuff',
                            'teleport', 'webtrends', 'worm', 'yandex', 'freedom',
                            'livelapbot','help@dataminr.com','everyonesocialbot','tweetedtimes.com','metauri api']
        #
        # load blacklisted cities, countries, ips, user agents
        # at scale, a memchached solution would be better (say Snakr v2)
        #
        from models import CityLog, CountryLog, IPLog, HostLog, UserAgentLog
        self._blacklisted_cities        = self._load_blacklist(CityLog, 'cities', 'city')
        self._blacklisted_countries     = self._load_blacklist(CountryLog, 'countries', 'country')
        self._blacklisted_ips           = self._load_blacklist(IPLog, 'ips', 'ip')
        self._blacklisted_hosts         = self._load_blacklist(HostLog, 'hosts', 'host')
        self._blacklisted_useragents    = self._load_blacklist(UserAgentLog, 'useragents', 'useragent')
        self._event.log(event_type='I', message='Botdetector loaded.')

    def if_bot_then_403(self, request):
        ip_address, geo_lat, geo_long, geo_city, geo_country, http_host, http_useragent, http_referer = Utils.get_meta(request, True)
        #
        # at scale, this should be multithreaded/multi-processed in parallel
        # or implemented as a set of microservice lookups to a separate memcached lookup service
        #
        for bot in self._known_bots:
            if bot in http_useragent:
                raise self._event.log(request=request, event_type='B', messagekey='ROBOT', value='Known Bot {%}' % bot, status_code=-403)
        for bad in self._blacklisted_useragents:
            if http_useragent == bad:
                raise self._event.log(request=request, event_type='B', messagekey='ROBOT', value='Blacklisted Useragent {%s}' % http_useragent, status_code=-403)
        for bad in self._blacklisted_countries:
            if geo_country == bad:
                raise self._event.log(request=request, event_type='B', messagekey='ROBOT', value='Blacklisted Country {%s}' % geo_country, status_code=-403)
        for bad in self._blacklisted_cities:
            if geo_city == bad:
                raise self._event.log(request=request, event_type='B', messagekey='ROBOT', value='Blacklisted City {%s}' % geo_city, status_code=-403)
        for bad in self._blacklisted_hosts:
            if http_host == bad:
                raise self._event.log(request=request, event_type='B', messagekey='ROBOT', value='Blacklisted Host {%s}' % http_host, status_code=-403)
        for bad in self._blacklisted_ips:
            if ip_address == bad:
                raise self._event.log(request=request, event_type='B', messagekey='ROBOT', value='Blacklisted IP {%s}' % ip_address, status_code=-403)
        return

    def _load_blacklist(self, modelclass, pluralname, element):
        queryresults = modelclass.objects.filter(is_blacklisted='Y').values(element)
        listresults = [str(item[element]).lower() for item in list(queryresults)]
        self._event.log(event_type='I', message='  Cached %s blacklisted %s' % (len(listresults), pluralname))
        return listresults

