# Snakr 

A URL shortener service demo using [Python 2.7](https://www.python.org/) and [Django 1.5.11](https://www.djangoproject.com/)
on [Google App Engine](https://cloud.google.com/appengine) with a [Google Cloud SQL (1st Generation)](https://cloud.google.com/sql/) backend.

## Background 
URL shorteners are used to generate a smaller “abbreviated” version of a URL so that the smaller URL can be used as an alias in place of the longer URL. Subsequent calls to the smaller URL will redirect to the same resource originally identified by the longer URL, including all querystring parameters and other valid URL components. This is useful for several reasons:

Upside                                          | Reason
----------------------------------------------- | ------------------------------
Easier to use (“beautification”)                | It can be substantially easier to enter, copy, paste, manipulate, remember, or otherwise use a shorter URL rather than its longer version. Smaller is inherently “more beautiful” than longer.
Less prone to breakage                          | Longer URLs can be broken when embedded in documents, messages, etc. due to misentry, mispaste, line wrapping breakages, or cutoffs due to data length limitations in standards and tools like SMS or Twitter. Shorter URLs are less prone to these problems.
Less bandwidth used                             | Shorter URLs require less transmission sources that longer ones, a problem that increasingly manifests itself at scale.
Less storage used                               | If the URLs are stored, the shorter URL will use less space.
Increased security from URL payload malfeasance | URLs may contain payloads such as SQL injection, etc. in the query string or other components. A shortener that encodes and scrubs the URL first for safety can return a short URL that itself is guaranteed not to contain such issues (since it is generated), and on redirect to the longer URL return the longer URL’s safely encoded version.

There are downsides to URL shorteners:

Downside                                          | Reason
------------------------------------------------- | ------------------------------
Short URL as fraud enabler                        | Shorteners have been used to obfuscate the origin of traffic, beat blacklists, track user engagement activity surreptitiously, etc. Shortener services identified as trafficking in a lot of this can find themselves blacklisted, to the detriment of the service’s users and thus the service itself.
Negative effects on SEO, CTR, etc.                | Shortened URLs may not rank as high or at all in search engine results versus their longer URL parents. This could pose problems is use cases where SEO matters. The same goes true for uses where short URLs are delivered via ads or links exposed to end users who may not recognize them and thus be less likely to clickthru, thereby affecting monetization, traffic, campaign optimization, future campaign targeting accuracy, etc.

## Features Provided 
1.	A basic HTTP POST/GET interface is provided. 
    a.	POST is used to turn a long URL into a shortened URL.
    b.	A subsequent GET is used to redirect the shortened URL to its long URL target.
2.	URLs are cleansed and validate before shortening.
    a.	Only valid URLs are recongnized (see “Non-goals” #2 below for the definition of “valid”).
    b.	SSL/TLS is honored on both ends. HTTP long URLs create HTTP short URLs, while HTTPS long URLs create HTTPS short URLs. Ditto FTP and SFTP.
    c.	Per RFC 3986, schemas and domains/hosts/netlocs are treated as case-insensitive, while the rest of the URL is treated as case-sensitive. For example, three URLs identical in all aspects other than the schemas“http”, “hTtP”, and “HTTP” are all treated as identical and generate identical short URLs for the same .
    d.	The design and code should support global character sets. Additional testing would be needed here prior to production-ready.
3.	Duplicate long URLs submitted to the shortening service will generate only one short URL on the first call. Subsequent calls with the same long URL return the existing short URL.
4.	Short URL paths are generated from a random selection of DNS-safe characters (A-Z, a-z-, and 0-9, although the exact set of characters used can be modified via a metadata change). 
5.	The number of characters used defaults to 6; this is also modifiable up to 12 via a metadata change. 
6.	Easily-confused character combinations are excluded. No short URLs are generated which contain both:
    a.	A “0” (zero) and an “O” (uppercase letter ‘oh’), and/or;
    b.	A “1” (one) and a “l” (lowercase letter ‘ell’).
7.	If a collision is detected (a 2nd long url hash to the same short URL, an improbable occurance whose probablity defaults to 1 in 1.886 billion), the short URL is regenerated. This repeats until a unique short URL is generated. The number of max retries is set in the metadata as well, and defaults to 3. Increasing the size of the short URL generated by one in the MAXSIZE parameter in the metadata greatly increases the number of possible combinations at the expense of a short URL one character longer. If MAXSIZE is increased, old URLs using the smaller size still work, and you can even flip back to the old size later and both sizes will still resolve.

## Known Issues / Future Features
1. Django 1.5.11's SuspiciousOperation returns HTTP 500, not HTTP 400 (see http://stackoverflow.com/questions/35439621/django-suspiciousoperation-returns-as-http-500-on-google-app-engine-not-http-40). This means among other things that a badly formatted URL crashes WSGI, which is NOT good. This is my top priority to fix by applying the workaround mentioned in the StackOverflow page to run under Django 1.9.2 or latest possible.
2. Request filtering is not yet robust. Some non-supported requests will return HTTP 500 due to the previous issue.
3. There is no admin page or reporting. Will add that.
4. Geolocation detection is not working (see http://stackoverflow.com/questions/35492617/x-appengine-citylatlong-not-populated-on-google-app-engine-django-1-5-11-when-us). Will workaround or fix.
5. Other diagnostic/tracking info to be added to snakr_log.
6. snakr_log collects IPs with no encryption. This may not be legit for your applicable privacy and/or compliance needs. No other PII is collected. Check with your legal department or ex-spouse for all bad news.
7. Local testing with a local MySQL db was not tested or used with this. 
8. The GAE Development Environ was not tested or used with this. 
9. No test units are yet defined. It's a pretty simple app functionally; I'm not so sure this is really warranted.
10. No GAE endpoints for mobile are coded or supported. I may or may not add that. Feel free to do so.
11. Submission of a long url via a POST with a query string (e.g. "http://snakrv2.appspot.com/?u=http://www.shortenthisurlplease.com") may be added. Feel free to do so.
12. No aging or cleanup of URLs based on usage age-off or other rules is not provided. I did add a is_active status to support this in the future.
13. No other security or access features such as OAuth access control are provided. Access is controlled solely via the Google App Engine Authentication features.
14. Server 500 and other HTTP errors generated by the service are logged in the available Google Cloud logs which can be accessed via GAE Dashboard and if you are using it the Pycharm IDE. This catches a lot of bugs. No other syslogs or other logging access or monitoring is provided.


## URL Shortening Logic
#### On A POST Request ####
1. 

## Test It Online
1. Install curl or another REST client testing tool like [Advanced Rest Client Application for Chrome](https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo/reviews?hl=en-US&utm_source=ARC)

2. Using your REST testing tool, test the POST action:
    ```
    URL: http://snakrv2.appspot.com
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
   pip install -r requirements.txt -t lib
   ```
4. Create your GAE and Cloud SQL instances.

5. Upload from your Python IDE to GAE. I like [Pycharm](https://www.jetbrains.com/pycharm/).

6. Create an instance in Cloud SQL to hold the database.

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

11. In Settings.py, add your personal GAE config info, db connection info for your GAE Cloud SQL instance, then adjust these parameters accordingly:

Setting                | Value
---------------------- | ------------------------------
SHORTURL_HOST          | The root host (netloc) to append to the front of the short urls generated. Use your own small domain name for this and forward its traffic to your GAE public URL. The [GAE site](http://cloud.google.com) has instructions.
SHORTURL_PATH_SIZE     | How many characters in the 'shorten_using' alphabet to use in building short URLs, from 6 to 12. Note that this can be changed at will to a larger or smaller value between 6 and 12, and all historical short URLs will still work.
SHORTURL_PATH_ALPHABET | The alphabet containing the characters from which to build the short URL. This CANNOT be changed at will without possible breaking previously generated short URLs. This can occur if a character or digit is removed form the alphabet but which still appears in a previously-generated short URL. Those short URLs will break the next time they are used.
MAX_RETRIES            | The maximum number of retries to attempt before returning an error should a hashing collision occur (odds are appx 1 in 1.86 billion). Defaults to 3. No real need to change this.

### Installing Libraries
See the [Third party libraries](https://developers.google.com/appengine/docs/python/tools/libraries27)
page for libraries that are already included in the SDK.  To include SDK
libraries, add them in your app.yaml file. Other than libraries included in
the SDK, only pure python libraries may be added to an App Engine project.

## Author
Bret Lowery
