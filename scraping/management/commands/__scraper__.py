import pycurl
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


def save_url_image(field, url, name):
    r = requests.get(url)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    field.save(name, File(img_temp), save=True)

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
