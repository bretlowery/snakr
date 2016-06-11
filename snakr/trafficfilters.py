from patterns.singleton import Singleton
from secure.gae import gaeinit
gaeinit()
import loggr
from utilities import Utils
import secure.settings as settings
import urllib2
from django.utils import timezone
from snakr.models import CityLog, CountryLog, IPLog, HostLog, UserAgentLog, TPIpBls#
import ipaddr
import netaddr

class TrafficFilters():

    def __init__(self, *args, **kwargs):
        #
        # there can be only one
        # see Method 3 on http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
        #
        __metaclass__ = Singleton
        #
        self._event = loggr.SnakrEventLogger()
        if settings.ENABLE_BOTPROTECTION:
            self._event.log(event_type='I', message='Loading bot protection traffic filters')
            #
            # known bot list
            # all entries must be lowercase
            #
            self._known_bots = settings.BLACKLISTED_BOTS
            # bot whitelist
            self._whitelisted_bots=settings.WHITELISTED_BOTS
        else:
            self._event.log(event_type='I', message='Known bot filters not loaded; DISABLED in settings')
        if settings.ENABLE_BLACKLISTING:
            self._event.log(event_type='I', message='Loading blacklisting traffic filters')
            #
            # load blacklisted cities, countries, ips, user agents
            # at scale, a memchached solution would be better (say Snakr v2)
            #
            # from models import CityLog, CountryLog, IPLog, HostLog, UserAgentLog
            self._blacklisted_cities        = self._load_blacklist(CityLog, 'cities', 'city')
            self._blacklisted_countries     = self._load_blacklist(CountryLog, 'countries', 'country')
            self._blacklisted_ips           = self._load_blacklist(IPLog, 'ips', 'ip')
            self._blacklisted_hosts         = self._load_blacklist(HostLog, 'hosts', 'host')
            self._blacklisted_useragents    = self._load_blacklist(UserAgentLog, 'useragents', 'useragent')
            self._event.log(event_type='I', message='Traffic filters loaded.')
            #
            # Load any thirdparty daily IP lists
            #
            self._thirdparty_blacklisted_ips = []
            self.reload_thirdpartyblacklists()
        else:
            self._event.log(event_type='I', message='Blacklisting filters not loaded; DISABLED in settings')

    def filter_traffic(self, request):
        http_useragent = None
        #
        # bot checks
        #
        if settings.ENABLE_BOTPROTECTION:
            if not http_useragent:
                ip_address, geo_lat, geo_long, geo_city, geo_country, http_host, http_useragent, http_referer = Utils.get_meta(request, True)
            #
            # at scale, this should be multithreaded/multi-processed in parallel
            # or implemented as a set of microservice lookups to a separate memcached lookup service
            #
            whitelisted = False
            for ok in self._whitelisted_bots:
                if ok in http_useragent:
                    whitelisted = True
                    break
            if not whitelisted:
                for bot in self._known_bots:
                    if bot in http_useragent:
                        raise self._event.log(request=request, event_type='B', messagekey='ROBOT', value='Known Bot %s' % bot, status_code=-403)
        #
        # blacklisting checks
        #
        if settings.ENABLE_BLACKLISTING:
            if not http_useragent:
                ip_address, geo_lat, geo_long, geo_city, geo_country, http_host, http_useragent, http_referer = Utils.get_meta(request, True)
            for bad in self._blacklisted_useragents:
                if http_useragent == bad:
                    raise self._event.log(request=request, event_type='B', messagekey='BLACKLIST', value='Blacklisted Useragent %s' % http_useragent, status_code=-403)
            for bad in self._blacklisted_countries:
                if geo_country == bad:
                    raise self._event.log(request=request, event_type='B', messagekey='BLACKLIST', value='Blacklisted Country %s' % geo_country, status_code=-403)
            for bad in self._blacklisted_cities:
                if geo_city == bad:
                    raise self._event.log(request=request, event_type='B', messagekey='BLACKLIST', value='Blacklisted City %s' % geo_city, status_code=-403)
            for bad in self._blacklisted_hosts:
                if http_host == bad:
                    raise self._event.log(request=request, event_type='B', messagekey='BLACKLIST', value='Blacklisted Host %s' % http_host, status_code=-403)
            for bad in self._blacklisted_ips:
                if ip_address == bad:
                    raise self._event.log(request=request, event_type='B', messagekey='BLACKLIST', value='Blacklisted IP %s' % ip_address, status_code=-403)
            for bad in self._thirdparty_blacklisted_ips:
                if netaddr.valid_ipv6(ip_address):
                    if netaddr.valid_ipv6(bad):
                        if str(ipaddr.IPv6(bad)) == str(ipaddr.IPv6(ip_address)):
                            raise self._event.log(request=request, event_type='B', messagekey='BLACKLIST',
                                                  value='Third Party Blacklisted IP %s' % ip_address, status_code=-403)
                else:
                    if '-' in bad:
                        ipstart = IPv4ToInt(bad.split('-')[0])
                        ipend = IPv4ToInt(bad.split('-')[1])
                        if ipstart <= IPv4ToInt(ip_address) <= ipend:
                            raise self._event.log(request=request, event_type='B', messagekey='BLACKLIST',
                                                  value='Third Party Blacklisted IP %s' % ip_address, status_code=-403)
                    elif '/' in bad:
                        iprange = netaddr.glob_to_iptuple(netaddr.cidr_to_glob(bad))
                        ipstart = IPv4ToInt(str(iprange[0]))
                        ipend = IPv4ToInt(str(iprange[1]))
                        if ipstart <= IPv4ToInt(ip_address) <= ipend:
                            raise self._event.log(request=request, event_type='B', messagekey='BLACKLIST',
                                                  value='Third Party Blacklisted IP %s' % ip_address, status_code=-403)
                    elif bad == ip_address:
                            raise self._event.log(request=request, event_type='B', messagekey='BLACKLIST',
                                                  value='Third Party Blacklisted IP %s' % ip_address, status_code=-403)
        return

    def _load_blacklist(self, modelclass, pluralname, element):
        queryresults = modelclass.objects.filter(is_blacklisted='Y').values(element)
        listresults = [str(item[element]).lower() for item in list(queryresults)]
        self._event.log(event_type='I', message='  Cached %s blacklisted %s' % (len(listresults), pluralname))
        return listresults

    def _load_thirdpartyblacklists(self):
        self.reload_thirdpartyblacklists()

    def reload_thirdpartyblacklists(self):
        if settings.THRIDPARTY_BLACKLISTS:
            self._thirdparty_blacklisted_ips = []
            t = 0
            s = 0
            f = 0
            for thirdparty_blacklist_setting in settings.THRIDPARTY_BLACKLISTS:
                thirdparty_blacklist_name = thirdparty_blacklist_setting[0]
                self._event.log(event_type='I', message='(Re)loading daily %s...' % thirdparty_blacklist_name)
                thirdparty_blacklist_url = thirdparty_blacklist_setting[1]
                t += 1
                if not Utils.is_url_valid(thirdparty_blacklist_url):
                    self._event.log(event_type='W', message='Third Party blacklist %s at %s is not a valid URL; skipped.' % (thirdparty_blacklist_name, thirdparty_blacklist_url))
                    f += 1
                else:
                    try:
                        thirdparty_blacklist = urllib2.urlopen(thirdparty_blacklist_url)
                    except urllib2.HTTPError as e:
                        self._event.log(event_type='W',
                                        message='Third Party blacklist %s at %s raised error `%s`; skipped.' % (
                                        thirdparty_blacklist_name, thirdparty_blacklist_url, e.message))
                        f += 1
                    else:
                        pass
                    if not thirdparty_blacklist:
                        self._event.log(event_type='W',
                                        message='Third Party blacklist %s at %s could not be loaded; skipped.' % (
                                            thirdparty_blacklist_name, thirdparty_blacklist_url))
                        f += 1
                    else:
                        ip_blacklist = self._load_thirdparty_blacklist(thirdparty_blacklist_name, thirdparty_blacklist_url, thirdparty_blacklist)
                        self._thirdparty_blacklisted_ips.extend(ip_blacklist)
                        s += 1
            # for testing # self._thirdparty_blacklisted_ips.append('2601:00cf:8105:03df:2cbb:e004:aec5:6f02')
            self._thirdparty_blacklisted_ips = list(set(self._thirdparty_blacklisted_ips))  # trick to remove duplicate ips
            u = len(self._thirdparty_blacklisted_ips)
            self._event.log(event_type='I', message='Third Party blacklist loads completed: %s total, %s successfully loaded w/%s unique IPs/ranges, %s failed' % (t,s,u,f))
        return


    def _load_thirdparty_blacklist(self, thirdparty_blacklist_name, thirdparty_blacklist_url, thirdparty_blacklist):
        dt = timezone.now()
        blhash = Utils.get_hash(thirdparty_blacklist_name)
        try:
            bl = TPIpBls.objects.filter(id=blhash).get()
            c = bl.count()
        except:
            c = 0
            pass
        if c == 0:
            bl = TPIpBls(id=blhash, name=thirdparty_blacklist_name, download_from_url=thirdparty_blacklist_url,
                         first_loaded_on=dt, last_loaded_on=None)
            bl.save()
            bl = TPIpBls.objects.filter(id=blhash).get()
        t = 0
        s = 0
        f = 0
        ip_list = []
        for line in thirdparty_blacklist:
            line = line.lstrip().rstrip()
            if line[0] != '#':
                t += 1
                if '-' in line:
                    ipstart = line.split('-')[0]
                    ipend = line.split('-')[1]
                    if netaddr.valid_ipv4(ipstart) and netaddr.valid_ipv4(ipend):
                        ip_list.append(ipstart+'-'+ipend)
                        s += 1
                    else:
                        f += 1
                elif '/' in line:
                    ip = line.split('/')[0]
                    mask = line.split('/')[1]
                    if netaddr.valid_ipv4(ip):
                        if str(mask).isdigit():
                            if 0 <= int(mask) <= 32:
                                ip_list.append(ip+'/'+mask)
                                s += 1
                            else:
                                f += 1
                        else:
                            f += 1
                    else:
                        f += 1
                else:
                    if netaddr.valid_ipv4(line) or netaddr.valid_ipv6(line):
                        ip_list.append(line)
                        s += 1
                    else:
                        f += 1
        if s > 0:
            ip_list = list(set(ip_list))  # trick to remove duplicate ips
            bl.last_loaded_on = dt
            bl.save()
        self._event.log(event_type='I', message='     %s entries found, expanded to %s IPs loaded successfully, %s entries failed and skipped.' % (t,s,f))
        return ip_list


def IPv4ToInt(ip_address):
        return reduce(lambda a,b: a<<8 | b, map(int, ip_address.split(".")))
