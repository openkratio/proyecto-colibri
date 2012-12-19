import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import xml.etree.ElementTree as ET
from datetime import datetime
from bs4 import BeautifulSoup
from scraping.scraper import create_curl, get_file
from settings import VOTACIONES_URL
from zipfile import ZipFile

def parser_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    
    resumen = root.find('Informacion')
    print 'Sesion:', resumen.find('Sesion').text
    print 'Numero de votacion:', resumen.find('NumeroVotacion').text
    print 'Fecha:', resumen.find('Fecha').text
    print 'Titulo:', resumen.find('Titulo').text
    print 'Texto Expediente:', resumen.find('TextoExpediente').text
    print 'Titulo SubGrupo:', resumen.find('TituloSubGrupo').text
    print 'Texto SubGrupo:', resumen.find('TextoSubGrupo').text
    
    totales = root.find('Totales')
    asentimiento = totales.find('Asentimiento').text
    if asentimiento == 'No':
        print 'SE VOTA:'
        print '--------------'
        print 'Presentes:', totales.find('Presentes').text
        print 'A favor:', totales.find('AFavor').text
        print 'En contra:', totales.find('EnContra').text
        print 'No votan:', totales.find('NoVotan').text
        votaciones = root.find('Votaciones')
        for voto in votaciones:
            print '\t', voto.find('Asiento').text, voto.find('Diputado').text, voto.find('Voto').text
        print 'Numero de votaciones', len(votaciones)
    else:
        print 'SE ASIENTE'

def extract_files(pathzip):
    basedir = os.path.dirname(pathzip)
    xmlzip =  ZipFile(pathzip, 'r')
    xmlzip.extractall(basedir)
    xmlzip.close()
    os.remove(pathzip)
    for xml in os.listdir(basedir):
        parser_xml(basedir + '/' + xml)
        os.remove(basedir + '/' + xml)

    os.rmdir(os.path.dirname(pathzip))

#get zip
now = datetime.now().strftime('%Y/%m/13')
now_file = datetime.now().strftime('%Y%m13')
url = VOTACIONES_URL + now
votaciones_curl = create_curl(url)
votaciones_curl.perform()
if votaciones_curl.getinfo(votaciones_curl.HTTP_CODE) == 200:
    html_doc = votaciones_curl.body.getvalue()
    soup = BeautifulSoup(html_doc)

    xml_soup = soup.find(lambda tag: tag.name == 'a' and tag.parent.name == 'td')
    if xml_soup:
        xml_url = 'http://www.congreso.es' + xml_soup.attrs['href']
        pathzip = '/tmp/votaciones' + now_file
        if os.path.isdir(pathzip):
            os.rmdir(pathzip)
        os.mkdir(pathzip)
        get_file(xml_url.encode('utf8'), pathzip + '/xmls.zip')
        extract_files(pathzip + '/xmls.zip')
votaciones_curl.close()
