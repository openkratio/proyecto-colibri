# -*- coding: utf-8 -*-

import pycurl
import os, sys
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from bs4 import BeautifulSoup

def create_curl(url):
    curl = pycurl.Curl()
    curl.url = url
    curl.body = StringIO()
    curl.http_code = -1
    curl.setopt(curl.URL, curl.url)
    curl.setopt(curl.WRITEFUNCTION, curl.body.write)

    return curl

#Get urls
root_url = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DiputadosLegFechas"
url_fichas = []

url = root_url
has_next = True

while(has_next):
    curl_request = create_curl(url)
    curl_request.perform()
    html_doc = curl_request.body.getvalue()
    curl_request.close()
    soup = BeautifulSoup(html_doc)
    list_dip = soup.findAll(lambda tag: tag.name == 'a' and tag.parent.name == 'li' and tag.has_key('class'), "")
    for dip in list_dip:
        url_fichas.append(dip.attrs['href'].__str__())

    paginacion = soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'ul' and tag.has_key('class'), "", text='Página Siguiente')
    if not paginacion:
        has_next = False
    else:
        url = paginacion.attrs['href'].__str__()


#TODO request url_fichas and save diputado model instances
print len(url_fichas)
