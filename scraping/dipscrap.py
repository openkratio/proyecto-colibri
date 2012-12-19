# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.diputado import Diputado, Asiento
from models.partido import Partido, Grupo
from mongoengine import connect
import re
from settings import DIPUTADOS_URL, DATABASE, PROJECT_DIR
from scraper import create_curl
from bs4 import BeautifulSoup

def get_urls():
    url = DIPUTADOS_URL
    has_next = True
    url_fichas = []

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

        #has_next = False

    return url_fichas

def get_dips(url_fichas):
    m = []
    for url in url_fichas:
        curl = create_curl(url)
        curl.perform()
        curl.http_code = curl.getinfo(curl.HTTP_CODE)
        m.append(curl)
        curl.close()

    return m

def parser_dip(m):
    connection = connect(DATABASE)
    # get result
    for c in m:
        print "%-53s http_code %3d" % (c.url, c.http_code)
        
        if c.http_code == 200:
            html_doc = c.body.getvalue()
            soup = BeautifulSoup(html_doc)

            cv_soup = soup.find(id='curriculum')
            if cv_soup:
                
                datos_diputado = soup.find(id='datos_diputado')

                exist_dip = Diputado.objects(ficha=c.url)
                if exist_dip:
                    dip_instance = exist_dip[0]
                else:
                    dip_instance = Diputado()

                #get name
                nombre_soup = cv_soup.find('div', 'nombre_dip')
                if nombre_soup:
                    dip_instance.nombre = nombre_soup.text.split(',')[1].strip().encode('utf8')
                    dip_instance.apellidos = nombre_soup.text.split(',')[0].strip().encode('utf8')

                #get url
                dip_instance.ficha = c.url

                #get email
                correo_soup = cv_soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'div' and tag.has_key('title'), text=re.compile("([a-zA-Z0-9]*[\.])*@congreso.es"))
                if correo_soup:
                    dip_instance.correo = correo_soup.text.split()[0].encode('utf8')

                #get web
                web_soup = cv_soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'div' and tag.has_key('title'), text=re.compile("https?:\/\/"))
                if web_soup:
                    dip_instance.web = web_soup.attrs['href'].encode('utf8')

                #get twitter
                twitter_soup = cv_soup.findAll(lambda tag: tag.name == 'img' and tag.parent.name == 'a',src=re.compile("codigoTipoDireccion=tw"))
                if twitter_soup:
                    dip_instance.twitter = twitter_soup[0].parent.attrs['href'].encode('utf8')

                #get circunscripcion
                circuns_soup = cv_soup.find('div', 'dip_rojo', text=re.compile("Diputad[ao] por [a-zA-Z]?"))
                if circuns_soup:
                    circuns_soup = re.sub(r'Diputad[ao] por ', '' ,circuns_soup.text).strip()
                    circuns_soup = re.sub(r'\.$', '' ,circuns_soup)
                    dip_instance.circunscripcion = circuns_soup.encode('utf8')

                #get grupo
                grupo_soup = cv_soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'div', text=re.compile("G\.P\. .* \( [a-zA-Z]+ \)"))
                if grupo_soup:
                    grupo_match = re.search('^G\.P\. (.+) (\( [a-zA-Z]+ \))',grupo_soup.text, re.M|re.I)
                    if grupo_match:
                        grupo_nombre = grupo_match.group(1).strip().encode('utf8')
                        grupo_acronimo = grupo_match.group(2).strip().encode('utf8')
                        grupo_instance = Grupo()
                        grupo_instance.nombre = grupo_nombre
                        grupo_instance.acronimo = grupo_acronimo

                #get partido
                partido_soup = soup.find('p', 'nombre_grupo')
                if partido_soup:
                    partido_nombre = partido_soup.text.strip().encode('utf8')
                    partido_instance = Partido()
                    partido_instance.nombre = partido_nombre
                    
                    if datos_diputado:
                        logo_partido = datos_diputado.find(lambda tag: tag.name == 'img' and tag.parent.name == 'a')
                        if logo_partido:
                            logo_url = 'http://www.congreso.es' + logo_partido.attrs['src']
                            partido_instance.logo = PROJECT_DIR + '/static/images/logos/' + logo_url.split('/')[-1].encode('utf8')
                            logo_curl = create_curl(logo_url.encode('utf8'))
                            logo_curl.perform()
                            f = open("%s" % (partido_instance.logo,), 'wb')
                            f.write(logo_curl.body.getvalue())
                            f.close()
                            logo_curl.close()

                            partido_instance.web = logo_partido.parent.attrs['href'].encode('utf8')

                    if grupo_soup:
                        partido_instance.grupo = grupo_instance
                    
                    dip_instance.partido = partido_instance

                #get asiento
                if datos_diputado:
                    asiento_soup = datos_diputado.find('p', 'pos_hemiciclo').find('img')
                    if asiento_soup:
                        asiento_url = 'http://www.congreso.es' + asiento_soup.attrs['src']
                        asiento_instance = Asiento()
                        asiento_instance.imagen = PROJECT_DIR + '/static/images/asientos/' + asiento_url.split('/')[-1].encode('utf8')
                        asiento_curl = create_curl(asiento_url.encode('utf8'))
                        asiento_curl.perform()
                        f = open("%s" % (asiento_instance.imagen,), 'wb')
                        f.write(asiento_curl.body.getvalue())
                        f.close()
                        asiento_curl.close()
                        dip_instance.asiento = asiento_instance

                #get foto
                if datos_diputado:
                    foto_soup = datos_diputado.find(lambda tag: tag.name == 'img' and tag.parent.name == 'p')
                    if foto_soup:
                        foto_url = 'http://www.congreso.es' + foto_soup.attrs['src']
                        dip_instance.foto = PROJECT_DIR + '/static/images/fotos/' + foto_url.split('/')[-1].encode('utf8')
                        foto_curl = create_curl(foto_url.encode('utf8'))
                        foto_curl.perform()
                        f = open("%s" % (dip_instance.foto,), 'wb')
                        f.write(foto_curl.body.getvalue())
                        f.close()
                        foto_curl.close()

                dip_instance.save()

                print "**********", dip_instance.nombre, "**********"
                print "************************************************************************************************"

    connection.disconnect()

#Get urls
url_fichas = get_urls()

#Get dips
if len(url_fichas) > 0:
    m = get_dips(url_fichas)
    parser_dip(m)
