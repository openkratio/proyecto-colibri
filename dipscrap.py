# -*- coding: utf-8 -*-
import pycurl
import os, sys
from models.diputado import Diputado
from mongoengine import connect
import re

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


m = pycurl.CurlMulti()
m.handles = []

for url in url_fichas:
    curl = create_curl(url)
    m.handles.append(curl)
    m.add_handle(curl)

print "get diputados"

# get data
num_handles = len(m.handles)
while num_handles:
    while 1:
        ret, num_handles = m.perform()
        if ret != pycurl.E_CALL_MULTI_PERFORM:
            break
    m.select(1.0)

# close handles
for c in m.handles:
    c.http_code = c.getinfo(c.HTTP_CODE)
    m.remove_handle(c)
    c.close()
m.close()



print "parsing"
connection = connect('colibri_db')
# get result
for c in m.handles:
    html_doc = c.body.getvalue()
    soup = BeautifulSoup(html_doc)
    dip_instance = Diputado()
    
    nombre_soup = soup.find(id='curriculum').find('div', 'nombre_dip')
    if nombre_soup:
        dip_instance.nombre = nombre_soup.text.split(',')[1]
        dip_instance.apellidos = nombre_soup.text.split(',')[0]
    
    dip_instance.ficha = c.url
    
    correo_soup = soup.find(id='curriculum').find(lambda tag: tag.name == 'a' and tag.parent.name == 'div' and tag.has_key('title'), text=re.compile("([a-zA-Z0-9]*[\.])*@congreso.es"))
    if correo_soup:
        dip_instance.correo = correo_soup.text.split()[0]
    
    web_soup = soup.find(id='curriculum').find(lambda tag: tag.name == 'a' and tag.parent.name == 'div' and tag.has_key('title'), text=re.compile("https?:\/\/"))
    if web_soup:
        dip_instance.web = web_soup.attrs['href']
    
    twitter_soup = soup.find(id='curriculum').findAll(lambda tag: tag.name == 'img' and tag.parent.name == 'a',src=re.compile("codigoTipoDireccion=tw"))
    if twitter_soup:
        dip_instance.twitter = twitter_soup[0].parent.attrs['href']

    dip_instance.save()

    print "**********", c.url, "**********"
    print "%-53s http_code %3d, %6d bytes" % (c.url, c.http_code, len(html_doc))

connection.disconnect()
