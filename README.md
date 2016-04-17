# Snakr v1.0.6

A URL shortener service demo using [Python 2.7](https://www.python.org/) and [Django 1.9](https://www.djangoproject.com/)
on [Google App Engine](https://cloud.google.com/appengine) with a [Google Cloud SQL (1st Generation)](https://cloud.google.com/sql/) and [Google Datastore](https://cloud.google.com/datastore/) backend. 
The install loads Django 1.9, overriding GAE's Django 1.5.11 supported (as of 3/2016) install.

This is intended as a learning exercise, so it does not use the [Google URL Shortener API](https://developers.google.com/url-shortener/).

**v1.0.1**
Supports Django 1.9 on Google App Engine.

**v1.0.2** 
Adds optional database event logging, basic bot/crawler blocking, and optional blacklisting at the city, country, IP, http host, and/or http useragent levels.

**v1.0.3** 
Corrected target page title extraction; other bug fixes.

**v1.0.4**
More bug fixes.

**v1.0.5**
Rolled back due to GAE bug.

**v1.0.6**
Added support for writing the event stream to either Google Cloud SQL (MySQL) and/or Google Datastore (NoSQL). Cloud SQL supports a traditional star schema while the Datastore uses a versioned, schemaless structure.


## Background 
URL shorteners are used to generate a smaller “abbreviated” version of a URL so that the smaller URL can be used as an alias in place of the longer URL. Subsequent calls to the smaller URL will redirect to the same resource originally identified by the longer URL, including all querystring parameters and other valid URL components. This is useful for several reasons:

Upside                                          | Reason
----------------------------------------------- | ------------------------------
Easier to use (“beautification”)                | It can be substantially easier to enter, copy, paste, manipulate, remember, or otherwise use a shorter URL rather than its longer version. Smaller is inherently “more beautiful” than longer.
Less prone to breakage                          | Longer URLs can be broken when embedded in documents, messages, etc. due to misentry, mispaste, line wrapping breakages, or cutoffs due to data length limitations in standards and tools like SMS or Twitter. Shorter URLs are less prone to these problems.
Less bandwidth used                             | Shorter URLs require less transmission sources that longer ones, a problem that increasingly manifests itself at scale.
Less storage used                               | If the URLs are stored, the shorter URL will use less space.

There are downsides to URL shorteners:

Downside                                                | Reason
------------------------------------------------------- | ------------------------------
Short URL as fraud enabler                              | Shorteners have been used to obfuscate the origin of traffic, beat blacklists, track user engagement activity surreptitiously, etc. Shortener services identified as trafficking in a lot of this can find themselves blacklisted, to the detriment of the service’s users and thus the service itself.
Short URLs can hide payload malfeasance in the long URL | URLs may contain payloads such as SQL injection, etc. in the query string or other components. A shortener that encodes and scrubs the URL first for safety can return a short URL that itself is guaranteed not to contain such issues (since it is generated), but return them to the caller when resolved to the long URL.
Negative effects on SEO, CTR, etc.                      | Shortened URLs may not rank as high or at all in search engine results versus their longer URL parents. This could pose problems is use cases where SEO matters. The same is true when short URLs are delivered via ads or links exposed to end users who may not recognize them and thus be less likely to clickthru, thereby affecting monetization, traffic, campaign optimization, future campaign targeting accuracy, etc.

## Performance

Snakr can create and return a short url in under 200ms. I haven't load tested this at volume but assume GC can handle growth.

## Features Provided 

**NEW IN 1.0.6**
Events can be optionally logged to Google Cloud SQL (when settings.DATABASE_LOGGING = True and settings.PERSIST_EVENTSTREAM_TO_CLOUDSQL = True) and/or Google Datastore ((when settings.DATABASE_LOGGING = True and settings.PERSIST_EVENTSTREAM_TO_DATASTORE = True). Events are always logged to Google App Engine logging.

**Existing Features**
1.	A basic HTTP POST/GET interface is provided. 
  1.	POST is used to turn a long URL into a shortened URL.
  2.	A subsequent GET is used to redirect the shortened URL to its long URL target.
    
2.	URLs are cleansed and validate before shortening.
  1. Only valid URLs are recongnized (see “Non-goals” #2 below for the definition of “valid”).
  2. SSL/TLS is honored on both ends. HTTP long URLs create HTTP short URLs, while HTTPS long URLs create HTTPS short URLs. Ditto FTP and SFTP.
  3. Per RFC 3986, schemas and domains/hosts/netlocs are treated as case-insensitive, while the rest of the URL is treated as case-sensitive. For example, three URLs identical in all aspects other than the schemas“http”, “hTtP”, and “HTTP” are all treated as identical and generate identical short URLs for the same .
  4. The design and code should support global character sets. Additional testing would be needed here prior to production-ready.

3.	Duplicate long URLs submitted to the shortening service will generate only one short URL on the first call. Subsequent calls with the same long URL return the existing short URL.

4.	Short URL paths are generated from a random selection of DNS-safe characters (A-Z, a-z-, and 0-9, although the exact set of characters used can be modified via a metadata change). 

5.	The number of characters used defaults to 6; this is also modifiable up to 12 via a metadata change. 

6.	Easily-confused character combinations are excluded. No short URLs are generated which contain both:
  1. A “0” (zero) and an “O” (uppercase letter ‘oh’), and/or;
  2. A “1” (one) and a “l” (lowercase letter ‘ell’).

7.	If a collision is detected (a 2nd long url hash to the same short URL, an improbable occurance whose probablity defaults to 1 in 1.886 billion), the short URL is regenerated. This repeats until a unique short URL is generated. The number of max retries is set in the metadata as well, and defaults to 3. Increasing the size of the short URL generated by one in the MAXSIZE parameter in the metadata greatly increases the number of possible combinations at the expense of a short URL one character longer. If MAXSIZE is increased, old URLs using the smaller size still work, and you can even flip back to the old size later and both sizes will still resolve.

8.  Basic bot and crawler blocking is available. A blacklist of known bot user agent strings is provided. Any request coming from a user agent containing one of the strings in the blacklist will be 403d.

## Known Issues / Future Features
1. Django 1.5.11's SuspiciousOperation returns HTTP 500, not HTTP 400 (see http://stackoverflow.com/questions/35439621/django-suspiciousoperation-returns-as-http-500-on-google-app-engine-not-http-40). This means among other things that a badly formatted URL crashes WSGI, which is NOT good. This is my top priority to fix by applying the workaround mentioned in the StackOverflow page to run under Django 1.9.2 or latest possible.

   **UPDATE:** v1.0.0 I worked around this by implementing a custom /django/core/handlers/base.py that includes Django 1.9's SuspiciousOperation exception block with some minor changes. Unknown short URLs etc. now return HTPP 400 with a meaningful error message.

   **UPDATE:** v1.0.1 Fixed by implementing Django 1.9 

2. Request filtering is not yet robust. Some non-supported requests will return HTTP 500 due to the previous issue.

   **UPDATE:** v1.0.0 Much improved. Not fully tested yet. Haven't gone through all of the use cases.

   **UPDATE:** v1.0.1 Fixed by implementing Django 1.9 and a few bug fixes

3. There is no admin page or reporting. Will add that.

4. Geolocation detection is not working (see http://stackoverflow.com/questions/35492617/x-appengine-citylatlong-not-populated-on-google-app-engine-django-1-5-11-when-us). Will workaround or fix.

   **UPDATE:** v1.0.0 Fixed  
   
5. Other diagnostic/tracking info to be added to snakr_log.

   **UPDATE:** v1.0.0 Added storage for some of these. Looks like I'm hinting that I'm adding a robust demo fraud and abuse detection system later.

   **UPDATE:** v1.0.1 Logging now removed from the db and placed into json logging files.

6. snakr_log collects IPs with no encryption. This may not be legit for your applicable privacy and/or compliance needs. No other PII is collected. Check with your legal department or ex-spouse for all bad news.

   **UPDATE:** v1.0.0 I encode these now into binary(128). This is for minimizing storage, NOT for encryption. They are NOT encrypted and can be reversed into the original readable IPs.

   **UPDATE:** v1.0.1 Logging now removed from the db and placed into json logging files.
   
7. Local testing with a local MySQL db was not tested or used with this.

   **UPDATE:** v1.0.1 Local dev and QA now supported using local dev_appserver.py against either local MySQL or remote GCS.

8. The GAE Development Environ was not tested or used with this.

   **UPDATE:** v1.0.1 Local dev and QA now supported using local dev_appserver.py against either local MySQL or remote GCS.

9. No test units are yet defined. It's a pretty simple app functionally; I'm not so sure this is really warranted.

10. No GAE endpoints for mobile are coded or supported. I may or may not add that. Feel free to do so.

11. Submission of a long url via a POST with a query string (e.g. "http://snakr.appspot.com/?u=http://www.shortenthisurlplease.com") may be added. Feel free to do so.

   **UPDATE:** v1.0.0 I'm going to add this shortly, no pun intended. Some code already implemented for this.

   **UPDATE:** v1.0.1 CANCELLED: this makes the app vulnerable to certain attacks when the GET is redirected into a PUT. Not implementing.

12. No aging or cleanup of URLs based on usage age-off or other rules is not provided. I did add a is_active status to support this in the future.

13. No other security or access features such as OAuth access control are provided. Access is controlled solely via the Google App Engine Authentication features.

14. Server 500 and other HTTP errors generated by the service are logged in the available Google Cloud logs which can be accessed via GAE Dashboard and if you are using it the Pycharm IDE. This catches a lot of bugs. No other syslogs or other logging access or monitoring is provided.

15. You can buy a short domain name and have it CNAME to yourdomain.appspot.com and then change the settings.py to prepend your short URLs with the short domain. To support secure domain redirection, your short domain will need an SSL certificate and secure redirection enabled on your domain provider. 
Alternatively, you can use your short domain for short HTTP urls and yorudomain.appspot.com for short HTTPS urls. The relevant settings in settings.py are:

    ```
    # host (netloc) of the short URL to use for HTTP urls
    SHORTURL_HOST           = "bret.guru"  #change to your short domain
    
    # host (netloc) of the short URL to use for HTTPS urls
    SECURE_SHORTURL_HOST    = "snakr.appspot.com"
    ```
    
    
    This produces short URLs:
    
    ```
    http://bret.guru/xxxxxx
    https://snakr.appspot.com/xxxxxx
    ```
    
    Once you have your SSL certficate and secure redirection turned on, you can use the same short domain on both:
    
    ```
    SHORTURL_HOST           = "bret.guru"   
    SECURE_SHORTURL_HOST    = "bret.guru"
    ```
    
    producing:
    
    ```
    http://bret.guru/xxxxxx
    https://bret.guru/xxxxxx
    ```
    
    16. A mobile app/endpoints would be neat.
    
    
## Test It Online
1. Install curl or another REST client testing tool like [Advanced Rest Client Application for Chrome](https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo/reviews?hl=en-US&utm_source=ARC)

2. Using your REST testing tool, test the POST action:
    ```
    URL: http://bret.guru
    POST:
        Content-Type: application/json
        Payload:      {"u":"<the url you want to shorten goes here without the angle brackets>"}
    ```

3. Using your browser, curl or the tool, test the GET action:
    ```
    URL: <the short url generated by the POST step above>
    ```

## Install and Run
1. Install the [App Engine Python SDK](https://developers.google.com/appengine/downloads).
See the README file for directions. You'll need python 2.7 and [pip 1.4 or later](http://www.pip-installer.org/en/latest/installing.html) installed too.

2. Clone this repo with

   ```
   git clone https://github.com/bretlowery/snakr.git
   ```
3. Install dependencies in the project's lib directory.
   Note: App Engine can only import libraries from inside your project directory.

   ```
   cd snakr
   pip install -r requirements-local.txt -t lib
   pip install -r requirements-vendor.txt -t lib
   ```
   
4. Create your GAE and Cloud SQL instances.

5. Upload from your Python IDE to GAE. I use [Pycharm](https://www.jetbrains.com/pycharm/) as it has Google Cloud and GAE integration.

6. Create an instance in Cloud SQL to hold the database. You do not need to pre-create anything in Google Datastore. 

7. Create a user account in SQL to install the database such as "dbo" with a password. Do NOT use the sql "root" login and
do NOT change its existing password. GAE will use root@localhost to connect to Cloud SQL on the back end.

8. In your browser, visit WhatIsMyIP.com. Get your local IP address, and over in the Cloud SQL admin page, grant your IP access to
your SQL instance. This allows you to connect from your local machine. If your local IP changes, you will not be able to connect
from your local MySQL Workbench client until you grant your new IP acesss on the Cloud SQL admin page.

9. Install [MySQL Workbench](https://www.mysql.com/downloads) and connect to Cloud SQL using:
*Host = the Coud SQL IP (not your local one, the one of the Cloud SQL instance
*Port = the default 3306 MySQL port
*Username = "dbo", or the username you created
*Password = the password you entered
*Database/Scheme = the db/scheme name you entered

10. In MySQL Workbench, run install.sql to create the db objects.

11. In Settings.py, add your personal GAE config info, db connection info for your GAE Cloud SQL instance, etc. Adjust these parameters accordingly:

Setting                | Value
---------------------- | ------------------------------
ALLOWED_HOSTS          | A whitelist of all host names and IPs allowed to submit admin and POST requests to snakr.
CANONICAL_MESSAGES     | The list of snakr service error and warning messages.
DATABASE_LOGGING       | If True, logs events and request metadata into Google Cloud SQL (if PERSIST_EVENTSTREAM_TO_CLOUDSQL is also True) and/or Google Datastore (if PERSIST_EVENTSTREAM_TO_DATASTORE is also True).
ENABLE_LOGGING         | If True, logs service requests to the snakr log. False turns off logging.
GAE_APP_NAME           | "snakr"
GAE_APP_KEY            | The Google API key to use for the app. Provided by the Google API admin dashboard.
GAE_HOST               | Derived; DO NOT CHANGE.
GAE_PROJECT_ID         | The Google App Engine project ID from the GAE dashboard.
GCS_INSTANCE_NAME      | The Google Cloud SQL instance name as shown in the GCS dashboard.
INDEX_HTML             | If the SHORTURL_HOST or SECURE_SHORTURL_HOST value is entered into a browser with no path, it will redirect to this page.
LOG_HTTP200            | If true, logs HTTP 200 events such as short URL creation to the log.
LOG_HTTP302            | If true, logs HTTP 302 events such as short URL lookup and translation to the log.
LOG_HTTP400            | If true, logs HTTP 400 events to the log.
LOG_HTTP403            | If true, logs HTTP 403 events to the log.
LOG_HTTP404            | If true, logs HTTP 404 events to the log.
MAX_RETRIES            | The maximum number of retries to attempt before returning an error should a hashing collision occur (odds are appx 1 in 1.886 billion). Defaults to 3. No real need to change this.
MESSAGE_OF_LAST_RESORT | Catch-all error message if an exception occurs that's not in CANONICAL_MESSAGES._
OGTITLE                | If True, enable capture of the target long url's OpenGraph title ("og:title") and return it in the JSON along with the short url.
PERSIST_EVENTSTREAM_TO_CLOUDSQL | If True, and DATABASE_LOGGING is True, the event stream is logged to the Cloud SQL snakr_eventlog table and associated xxxLog dimension tables.
PERSIST_EVENTSTREAM_TO_DATASTORE | If True, and DATABASE_LOGGING is True, the event stream is logged in the Datastore as versioned EventStream entities.
RETURN_ALL_META        | If True, return all request metadata in the JSON at shorturl creation.
SECURE_SHORTURL_HOST   | The root host (netloc) to append to the front of the secure (HTTPS/SFTP) short urls generated. Use your own small domain name for this and forward its traffic to your GAE public URL. The [GAE site](http://cloud.google.com) has instructions.
SHORTURL_HOST          | The root host (netloc) to append to the front of the non-secure (HTTP/FTP) short urls generated. Use your own small domain name for this and forward its traffic to your GAE public URL. The [GAE site](http://cloud.google.com) has instructions.
SHORTURL_PATH_ALPHABET | The alphabet containing the characters from which to build the short URL. This CANNOT be changed at will without possible breaking previously generated short URLs. This can occur if a character or digit is removed form the alphabet but which still appears in a previously-generated short URL. Those short URLs will break the next time they are used.
SHORTURL_PATH_SIZE     | How many characters in the 'shorten_using' alphabet to use in building short URLs, from 6 to 12. Note that this can be changed at will to a larger or smaller value between 6 and 12, and all historical short URLs will still work.
SNAKRDB_DEBUG_DB       | When set to DEBUG and snakr is run locally from devappserver.py, local snakr will connect to remote GCS rather than local MySQL.
VERBOSE_LOGGING        | If True appends a JSON info record containing the requestor's IP, lat, long, user agent, host, city, and country of origin to the logging record for the URL request._


## Storage

Snakr persists its data in Google Cloud SQL in this version; later versions will use other storage options on Google Cloud such as Datastore or Memcached. This initial design uses three Cloud SQL tables.

The original design had both long and short urls in a single table. I split it in two thinking about future features such as multiple short URLs for a single long URL (useful in certain business-oriented use cases).

####Table snakr_longurl
One row per long URL successfully submitted for shortening to Snakr.

Column             | Datatype (all NOT NULL)  | Description
------------------ | ------------------------ | ------------
id (PK)            | BIGINT                   | 64-bit integer version of the hexdigest of the long integer hash of the quoted, utf8-encoded long URL. It's more efficient to lookup a long url using an integer key rather than comparing to the full VARCHAR long url.
longurl            | VARCHAR(4096)            | The quoted, utf8-encoded version of a long url successfully submitted for shortening to snakr.
created_on         | DATETIME                 | UTC datetimestamp of when the long URL was inserted into the table.
originally_encoded | CHAR(1)                  | "Y" if the longurl value was encoded when submitted, "N" otherwise. If an encoded long URL is submitted to snakr, it will be returned encoded when its short URL is submitted. Snakr does not alter original encodings.

####Table snakr_shorturl
One row per short URL successfully generated by Snakr.

Column             | Datatype (all NOT NULL)  | Description
------------------ | ------------------------ | ------------
id (PK)            | BIGINT                   | 64-bit integer version of the hexdigest of the long integer hash of the UNquoted, utf8-encoded short URL. It's more efficient to lookup a short url using an integer key rather than comparing to the full VARCHAR short url.
longurl_id (UK)    | BIGINT                   | The snakr_longurl.id value of the matching long URL to which the short URL redirects.
shorturl           | VARCHAR(40)              | The UNquoted, utf8-encoded version of the short URL generated by snakr.
shorturl_path_size | TINYINT                  | The value of settings.SHORTURL_PATH_SIZE at the time the short URL was generated. Used for snakr issue diagnosis/auditing.
created_on         | DATETIME                 | UTC datetimestamp of when the short URL was inserted into the table.
is_active          | CHAR(1)                  | "Y" on short URL creation. For future use to add short URL expiration and cleanup/purge functionality.
compression_ratio  | FLOAT                    | The ratio of short URL size to long URL size.

## Logging

Snakr uses standard Django logging which appears in the Google Cloud Logging console and can be downoaded via the Google Logging API. 

#### Cloud SQL Logging
In addition to standard request and state logging, Snakr also logs the following application-specific data elements to the log in JSON format, and to the snakrdb database if settings.DATABASE_LOGGING = True AND settings.PERSIST_EVENTSTREAM_TO_CLOUDSQL = True:

Element     | Value                | Default   | Description
------------| ---------------------| --------- | ------------
city        | string               | "none"    | If present, the geo location city name from X-AppEngine-City of the client calling Snakr. Used for tracking/diagnostics/forensics only. 
country     | string               | "none"    | If present, the geo location country name from X-AppEngine-Country of the client calling Snakr. Used for tracking/diagnostics/forensics only. 
host        | string               | "none"    | If present, the HTTP_HOST of the client. Used for tracking/diagnostics/forensics only.
ip          | IPv4 or IPv6 address | "none"    | If present, the IPv4 or IPv6 X-FORWARDED-FOR (if available) or REMOTE ADDR (if no X-FORWARDED-FOR is available) of the client calling Snakr. Used for tracking/diagnostics/forensics only.
lat         | float(10,8)          | 0.0       | If present, the geo location latitude from X-AppEngine-CityLatLong of the client calling Snakr. Used for tracking/diagnostics/forensics only. 0.0 means unknown, missing, not verified...
long        | float(11,8)          | 0.0       | If present, the geolocation longitude from X-AppEngine-CityLatLong of the client calling Snakr. Used for tracking/diagnostics/forensics only. 0.0 means unknown, missing, not verified...
longurl_id  | long                 | -1        | If present, the snakr_longurl.id value of the matching long URL redirected to by the short URL. -1 means unknown, missing, not specified, etc.
message     | string               | none      | Text message, such as an error or informational message.
shorturl_id | long                 | -1        | If present, the snakr_shorturl.id value of the matching short URL to which the long URL redirects. -1 means unknown, missing, not specified, etc.
status_code | integer              | 0         | If present, the HTTP status code that has or will be returned to the client.
referer     | string               | "none"    | If present, the HTTP_REFERER of the client.
ua          | string               | "none"    | If present, the HTTP__USER_AGENT of the client. Is useful for forensic cluster analysis for fraud or abuse patterns in the log.

If database logging is enabled, this information is stored in table **snakr_eventlog** and a set of associated dimension tables. The values above are stored in the tables below.

#### Table snakr_eventlog
One row per Snakr-submitted event.

Column             | Datatype (all NOT NULL)  | Description
------------------ | ------------------------ | ------------
id (PK)            | BIGINT                   | 64-bit auto incrementing integer; specifies the order in which events occurred.
logged_on          | DATETIME                 | Datetime at which the event was logged.
event_type         | CHAR(1)                  | B=Blacklisted/Bot (403), D=Debug, E=Error, I=Information, L=New LongURL Submitted (200), R=Existing Long URL Resubmitted (200), S=Short URL Redirect (302), W=Warning, X=Exception 
http_status_code   | INT                      | The HTTP status code retruned to the caller.
message            | VARCHAR(8192)            | Dev-defined text message
longurl_id         | BIGINT                   | The long URL hash of the long URL associated with the event, if any. If none, -1.
shorturl_id        | BIGINT                   | The short URL hash of the short URL associated with the event. If none, -1.
ip_id              | BIGINT                   | The 64-bit hash of the IP address of the origination of the event.
lat                | DECIMAL(10,8)            | The latitude of the client where the event originated, if any. If unknown, 0.
lng                | DECIMAL(11,8)            | The longitude of the client where the event originated, if any. If unknown, 0.
city_id            | BIGINT                   | The 64-bit hash of the city name of the origination of the event.
country_id         | BIGINT                   | The 64-bit hash of the country name of the origination of the event.
host_id            | BIGINT                   | The 64-bit hash of the HTTP_HOST of the origination of the event.
useragent_id       | BIGINT                   | The 64-bit hash of the HTTP_USER_AGENT submitted by the client in the request.
referer            | VARCHAR(2083)            | The HTTP_REFERER value submitted by the client in the request.

#### Table snakr_citylog
One row per city of traffic origination in any request to Snakr.

Column             | Datatype (all NOT NULL)  | Description
------------------ | ------------------------ | ------------
id (PK)            | BIGINT                   | The 64-bit hash of the city name of the origination of one or more events.
city               | VARCHAR(100)             | The city name of the origination of one or more events, from X-AppEngine-City.
is_blacklisted     | CHAR(1)                  | Y=The city is blacklisted. All requests from the city will be 403d. N=The city is not blacklisted. This is *not* queried per request, but cached at Snakr start. If this value is updated, Snakr must be restarted to recache the change.

#### Table snakr_countrylog
One row per country of traffic origination in any request to Snakr.

Column             | Datatype (all NOT NULL)  | Description
------------------ | ------------------------ | ------------
id (PK)            | BIGINT                   | The 64-bit hash of the country name of the origination of one or more events.
country            | VARCHAR(100)             | The country name of the origination of one or more events, from X-AppEngine-Country.
is_blacklisted     | CHAR(1)                  | Y=The country is blacklisted. All requests from the country will be 403d. N=The country is not blacklisted. This is *not* queried per request, but cached at Snakr start. If this value is updated, Snakr must be restarted to recache the change.

#### Table snakr_hostlog
One row per unique HTTP_HOST in any request to Snakr.

Column             | Datatype (all NOT NULL)  | Description
------------------ | ------------------------ | ------------
id (PK)            | BIGINT                   | The 64-bit hash of the HTTP_HOST of the origination of one or more events.
country            | VARCHAR(100)             | The HTTP_HOST of the origination of one or more events.
is_blacklisted     | CHAR(1)                  | Y=The host is blacklisted. All requests from the host will be 403d. N=The host is not blacklisted. This is *not* queried per request, but cached at Snakr start. If this value is updated, Snakr must be restarted to recache the change.

#### Table snakr_iplog
One row per unique absolute IPv4 or IPv6 address in any request to Snakr.

Column             | Datatype (all NOT NULL)  | Description
------------------ | ------------------------ | ------------
id (PK)            | BIGINT                   | The 64-bit hash of the absolute IPv4 or IPv6 address of the origination of one or more events.
ip                 | VARCHAR(45)              | The absolute IPv4 or IPv6 address of the origination of one or more events.
is_blacklisted     | CHAR(1)                  | Y=The IP is blacklisted. All requests from the IP will be 403d. N=The IP is not blacklisted. This is *not* queried per request, but cached at Snakr start. If this value is updated, Snakr must be restarted to recache the change.

#### Table snakr_useragentlog
One row per unique HTTP_USER_AGENT in any request to Snakr.

Column             | Datatype (all NOT NULL)  | Description
------------------ | ------------------------ | ------------
id (PK)            | BIGINT                   | The 64-bit hash of the HTTP_USER_AGENT of the origination of one or more events.
useragent          | VARCHAR(8192)            | The HTTP_USER_AGENT of the origination of one or more events.
is_blacklisted     | CHAR(1)                  | Y=The user agent is blacklisted. All requests from a client with this exact user agent will be 403d. N=The user agent is not blacklisted. This is *not* queried per request, but cached at Snakr start. If this value is updated, Snakr must be restarted to recache the change.


### Installing Libraries
See the [Third party libraries](https://developers.google.com/appengine/docs/python/tools/libraries27)
page for libraries that are already included in the SDK.  To include SDK
libraries, add them in your app.yaml file. Other than libraries included in
the SDK, only pure python libraries may be added to an App Engine project.

## Author
Bret Lowery
