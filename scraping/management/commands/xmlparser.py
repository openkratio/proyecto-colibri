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

class Command(BaseCommand):
    def parser_xml(self, file):

        print file
        tree = ET.parse(file)
        root = tree.getroot()
        resumen = root.find('Informacion')
        voting_instance, voting_created = Voting.objects.get_or_create(session=resumen.find('Sesion').text, number=resumen.find('NumeroVotacion').text)
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
                print vote
                member_name =  vote.find('Diputado').text.split(',')[1].strip()
                member_second_name =  vote.find('Diputado').text.split(',')[0].strip()
                member_instance = Member.objects.get(name=member_name, second_name=member_second_name)
                vote_instance, vote_created = Vote.objects.get_or_create(voting=voting_instance, member=member_instance)
                vote_instance.vote= vote.find('Voto').text
        else:
            voting_instance.save()

    def extract_files(self, pathzip):
        basedir = os.path.dirname(pathzip)
        xmlzip =  ZipFile(pathzip, 'r')
        xmlzip.extractall(basedir)
        xmlzip.close()
        os.remove(pathzip)
        for xml in os.listdir(basedir):
            self.parser_xml(basedir + '/' + xml)
            os.remove(basedir + '/' + xml)

        os.rmdir(os.path.dirname(pathzip))


    def handle(self, *args, **options):
        #get zip

        now = datetime.now().strftime('%Y/%m/%d')
        now_file = datetime.now().strftime('%Y%m%d')
        url = VOTACIONES_URL + now
        votaciones_curl = create_curl(url)
        votaciones_curl.perform()
        if votaciones_curl.getinfo(votaciones_curl.HTTP_CODE) == 200:
            html_doc = votaciones_curl.body.getvalue()
            votaciones_curl.close()
            soup = BeautifulSoup(html_doc)

            xml_soup = soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'td')
            if xml_soup:
                xml_url = 'http://www.congreso.es' + xml_soup.attrs['href']
                print xml_url
                pathzip = '/tmp/votaciones' + now_file
                if os.path.isdir(pathzip):
                    os.rmdir(pathzip)
                os.mkdir(pathzip)
                get_file(xml_url.encode('utf8'), pathzip + '/xmls.zip')
                self.extract_files(pathzip + '/xmls.zip')
        votaciones_curl.close()
