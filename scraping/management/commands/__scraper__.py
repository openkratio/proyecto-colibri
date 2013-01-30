import pycurl
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def save_url_image(field, url, name):
    r = requests.get(url)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    field.save(name, File(img_temp), save=True)

def get_url(url):
    r = requests.get(url)
    return r.content

def get_file(url, path):
    r = requests.get(url)
    f = open("%s" % (path,), 'wb')
    f.write(r.content)
    f.close()

