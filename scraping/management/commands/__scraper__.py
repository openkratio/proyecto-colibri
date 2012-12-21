import pycurl
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def create_curl(url):
    curl = pycurl.Curl()
    curl.url = url
    curl.body = StringIO()
    curl.http_code = -1
    curl.setopt(curl.URL, curl.url)
    curl.setopt(curl.WRITEFUNCTION, curl.body.write)
    curl.setopt(curl.CONNECTTIMEOUT, 30)
    curl.setopt(pycurl.TIMEOUT, 30)
    curl.setopt(pycurl.NOSIGNAL, 1)
    return curl
