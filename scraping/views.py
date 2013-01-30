from colibri.settings import GROUPS_URL
from bs4 import BeautifulSoup
import requests
from parliamentarygroup.models import *
from term.models import Term
from colibri.settings import GROUPS_URL, ACTUAL_TERM

TIMEOUT = 30

def save_url_image(field, url, name):
    r = requests.get(url, timeout=TIMEOUT)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    field.save(name, File(img_temp), save=True)

def get_url(url):
    r = requests.get(url, timeout=TIMEOUT)
    return r.content

def get_file(url, path):
    r = requests.get(url)
    f = open("%s" % (path,), 'wb')
    f.write(r.content)
    f.close()

def parser_group(html_group):
    soup = BeautifulSoup(html_group)
    name = soup.find('div', "TITULO_CONTENIDO", id="divTitulo")
    if name:
        return name.text

def scrap_group(url, term):
    if not Group.objects.filter(congress_url=url).exists():
        html_group = get_url(url)
        group_name = parser_group(html_group)
        term_instance = Term.objects.get(decimal=term )
        group_instance = Group(name= group_name, term= term_instance, congress_url=url)
        group_instance.save()

def scrap_groups(term=None):
    if not term:
        term = str(ACTUAL_TERM)
    url = GROUPS_URL + '&idLesgislatura=' + term
    html = get_url(url)
    soup = BeautifulSoup(html)
    groups_html = soup.findAll(lambda tag: tag.name == 'a' and tag.parent.name == 'li' and tag.parent.parent.name == 'ul' and tag.parent.parent.parent.name == 'div' and tag.has_key('class') and not tag.has_key('title'))
    for group in groups_html:
        scrap_group(group.attrs['href'], term)
