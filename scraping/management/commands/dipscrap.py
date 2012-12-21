# -*- coding: utf-8 -*-
import os, sys, time
from member.models import Member, MemberParty, Seat
from parliamentarygroup.models import Group, Party
import re
from colibri.settings import DIPUTADOS_URL, PROJECT_DIR
from __scraper__ import create_curl
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def get_urls(self):
        url = DIPUTADOS_URL
        has_next = True
        url_fichas = []

        while(has_next):
            time.sleep(1)
            curl_request = create_curl(url)
            try:
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
                has_next = False
            except:
                has_next = False

        return url_fichas

    def get_dips(self, url_fichas):
        m = []
        for url in url_fichas:
            time.sleep(1)
            curl = create_curl(url)
            try:
                curl.perform()
                curl.http_code = curl.getinfo(curl.HTTP_CODE)
                m.append(curl)
                curl.close()
            except:
                pass

        return m

    def parser_dip(self, m):
        # get result
        for curl in m:
            if curl.http_code == 200:
                html_doc = curl.body.getvalue()
                soup = BeautifulSoup(html_doc)

                cv_soup = soup.find(id='curriculum')
                if cv_soup:
                
                    datos_diputado = soup.find(id='datos_diputado')

                    member_instance, created = Member.objects.get_or_create(congress_web=curl.url)

                    #get name
                    soup_name = cv_soup.find('div', 'nombre_dip')
                    if soup_name:
                        member_instance.name = soup_name.text.split(',')[1].strip().encode('utf8')
                        member_instance.second_name = soup_name.text.split(',')[0].strip().encode('utf8')

                    #get url
                    member_instance.ficha = curl.url

                    #get email
                    soup_email = cv_soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'div' and tag.has_key('title'), text=re.compile("([a-zA-Z0-9]*[\.])*@congreso.es"))
                    if soup_email:
                        member_instance.email = soup_email.text.split()[0].encode('utf8')

                    #get web
                    soup_web = cv_soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'div' and tag.has_key('title'), text=re.compile("https?:\/\/"))
                    if soup_web:
                        member_instance.web = soup_web.attrs['href'].encode('utf8')

                    #get twitter
                    soup_twitter = cv_soup.findAll(lambda tag: tag.name == 'img' and tag.parent.name == 'a',src=re.compile("codigoTipoDireccion=tw"))
                    if soup_twitter:
                        member_instance.twitter = soup_twitter[0].parent.attrs['href'].encode('utf8')

                    #get division
                    soup_div = cv_soup.find('div', 'dip_rojo', text=re.compile("Diputad[ao] por [a-zA-Z]?"))
                    if soup_div:
                        soup_div = re.sub(r'Diputad[ao] por ', '' ,soup_div.text).strip()
                        soup_div = re.sub(r'\.$', '' ,soup_div)
                        member_instance.division = soup_div.encode('utf8')
                    """
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
                                get_file(logo_url.encode('utf8'), partido_instance.logo)
                                partido_instance.web = logo_partido.parent.attrs['href'].encode('utf8')

                        if grupo_soup:
                            partido_instance.grupo = grupo_instance
                    
                        member_instance.partido = partido_instance

                    #get asiento
                    if datos_diputado:
                        asiento_soup = datos_diputado.find('p', 'pos_hemiciclo').find('img')
                        if asiento_soup:
                            asiento_url = 'http://www.congreso.es' + asiento_soup.attrs['src']
                            asiento_instance = Asiento()
                            asiento_instance.imagen = PROJECT_DIR + '/static/images/asientos/' + asiento_url.split('/')[-1].encode('utf8')
                            get_file(asiento_url.encode('utf8'), asiento_instance.imagen)
                            member_instance.asiento = asiento_instance

                    #get foto
                    if datos_diputado:
                        foto_soup = datos_diputado.find(lambda tag: tag.name == 'img' and tag.parent.name == 'p')
                        if foto_soup:
                            foto_url = 'http://www.congreso.es' + foto_soup.attrs['src']
                            member_instance.foto = PROJECT_DIR + '/static/images/fotos/' + foto_url.split('/')[-1].encode('utf8')
                            get_file(foto_url.encode('utf8'), member_instance.foto)
                    """

                    member_instance.save()

    def handle(self, *args, **options):
        #Get urls
        url_fichas = self.get_urls()

        #Get dips
        if len(url_fichas) > 0:
            m = self.get_dips(url_fichas)
            self.parser_dip(m)
