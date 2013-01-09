# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from colibri.settings import VOTACIONES_URL
from zipfile import ZipFile
import os, sys, time
from member.models import Member
from vote.models import Voting, Vote
from __scraper__ import create_curl, save_url_image, get_file
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from colibri.settings import ACTUAL_TERM
import shutil
from colibri.settings import MEDIA_ROOT
import re

class Command(BaseCommand):
    def parser_xml(self, file):
        start_parser = datetime.now()
        tree = ET.parse(file)
        root = tree.getroot()
        resumen = root.find('Informacion')
        voting_instance, voting_created = Voting.objects.get_or_create(session=resumen.find('Sesion').text, number=resumen.find('NumeroVotacion').text)
        print voting_instance
        voting_instance.session = resumen.find('Sesion').text
        voting_instance.number = resumen.find('NumeroVotacion').text
        voting_instance.date = datetime.strptime(resumen.find('Fecha').text, "%d/%m/%Y")
        voting_instance.title = resumen.find('Titulo').text
        voting_instance.record_title = resumen.find('TextoExpediente').text
        voting_instance.subgroup_title = resumen.find('TituloSubGrupo').text if (resumen.find('TituloSubGrupo')) else "Empty"
        voting_instance.subgroup_text = resumen.find('TextoSubGrupo').text if (resumen.find('TextoSubGrupo')) else "Empty"
    
        totals = root.find('Totales')
        assent = totals.find('Asentimiento').text
        voting_instance.assent = assent
        if assent == 'No':
            voting_instance.attendee = int(totals.find('Presentes').text)
            voting_instance.for_votes = int(totals.find('AFavor').text)
            voting_instance.against_votes = int(totals.find('EnContra').text)
            voting_instance.no_votes = int(totals.find('NoVotan').text)
            voting_instance.abstains = int(totals.find('Abstenciones').text)

            voting_instance.save()
            votes = root.find('Votaciones')
            for vote in votes:
                member_name =  vote.find('Diputado').text.split(',')[1].strip()
                member_second_name =  vote.find('Diputado').text.split(',')[0].strip()
                member_instance = Member.objects.get(name=member_name, second_name=member_second_name)
                vote_instance, vote_created = Vote.objects.get_or_create(voting=voting_instance, member=member_instance)
                vote_instance.vote= vote.find('Voto').text
                vote_instance.save()
        else:
            voting_instance.save()
        finish_parser = datetime.now()
        print finish_parser - start_parser

    def extract_files(self, pathzip, pathunzip):
        print "extract"
        basedir = os.path.dirname(pathzip)
        try:
            xmlzip =  ZipFile(pathzip, 'r')
            xmlzip.extractall(pathunzip)
            xmlzip.close()
        except:
            print "delete %s" % (pathzip)
            os.remove(pathzip)

    def get_zip(self, xml_url, pathzip):
        print "get_zip"
        pathzips = MEDIA_ROOT + '/votes/zips'
        if not os.path.isdir(pathzips):
            os.mkdir(pathzips)
        if not os.path.exists(pathzip):
            print "download zip"
            get_file(xml_url.encode('utf8'), pathzip)

    def get_session(self, url):
        print "get %s" % (url)
        votaciones_curl = create_curl(url)
        votaciones_curl.perform()
        if votaciones_curl.getinfo(votaciones_curl.HTTP_CODE) == 200:
            html_doc = votaciones_curl.body.getvalue()
            votaciones_curl.close()
            soup = BeautifulSoup(html_doc)

            xml_soup = soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'td')
            if xml_soup:
                xml_url = 'http://www.congreso.es' + xml_soup.attrs['href']
                self.get_zip(xml_url)
        votaciones_curl.close()

    def handle(self, *args, **options):
        if args and args[0] == 'all':
            base_url1 = 'http://www.congreso.es/votaciones/OpenData?sesion='
            base_url2 = '&completa=1&legislatura=' + str(ACTUAL_TERM)
            first = 1
            last = 80
            for i in range(first, last):
                try:
                    url = base_url1 + str(i) + base_url2
                    print url
                    indexes = re.findall('[0-9]+', url, flags=0)
                    pathzip = MEDIA_ROOT + '/votes/zips/' + ''.join(indexes)  + '.zip'
                    pathxml = MEDIA_ROOT + '/votes/sessions/' + ''.join(indexes)
                    self.get_zip(url, pathzip)
                    if not os.path.isdir(pathxml):
                        self.extract_files(pathzip, pathxml)
                    if os.path.isdir(pathxml):
                        for xml in os.listdir(pathxml):
                            self.parser_xml(pathxml + '/' + xml)
                except Exception, e:
                    print pathzip
                    print e
        else:
            now = datetime.now().strftime('%Y/%m/%d')
            now_file = datetime.now().strftime('%Y%m%d')
            url = VOTACIONES_URL + now
            self.get_session(url)
