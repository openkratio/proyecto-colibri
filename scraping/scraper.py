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

def get_file(url, path):
    file_curl = create_curl(url)
    file_curl.perform()
    f = open("%s" % (path,), 'wb')
    f.write(file_curl.body.getvalue())
    f.close()
    file_curl.close()
