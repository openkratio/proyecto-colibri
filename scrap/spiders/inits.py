# coding=utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from bs4 import BeautifulSoup
from dateutil import parser as dparser
import re
import urlparse

from alerts.tasks import check_alert
from commission.models import Commission
from initiatives.models import Initiative
from member.models import Member
from parliamentarygroup.models import Group
import scrap.items as items
from term.models import Term

ACTUAL_TERM = Term.objects.latest('id')


class InitiativeSpider(CrawlSpider):
    name = 'initiatives'
    allowed_domains = ['congreso.es', ]
    start_urls = ['http://www.congreso.es/portal/page/portal/Congreso/'
                  'Congreso/Iniciativas/Indice de Iniciativas', ]
    rules = [
        Rule(SgmlLinkExtractor(
            allow=['/portal/page/portal/Congreso/Congreso/Iniciativas/Indice%'
                   '20de%20Iniciativas\?_piref73_1335503_73_1335500_1335500\.'
                   'next_page=/wc/servidorCGI&CMD=VERLST&BASE=IW10&PIECE=\w+&'
                   'FMT=INITXD1S\.fmt&FORM1=INITXLUS\.fmt&DOCS=\d+-\d+&QUERY='
                   '%28I%29\.ACIN1\.\+%26\+%28\d{3}%29\.SINI\.'], unique=True),
            'parse_initiative'),
        Rule(SgmlLinkExtractor(
            allow=['/portal/page/portal/Congreso/Congreso/Iniciativas/Indice'
                   '%20de%20Iniciativas\?_piref73_1335503_73_1335500_1335500\.'
                   'next_page=/wc/servidorCGI&CMD=VERLST&BASE=IW10&FMT=INITXLU'
                   'S\.fmt&DOCS=\d+-\d+&DOCORDER=FIFO&OPDEF=Y&QUERY=%28I%29\.'
                   'ACIN1\.\+%26\+%28\d{3}%29\.SINI\.'], unique=True),
            follow=True),]

    def parse_initiative(self, response):
        x = HtmlXPathSelector(response)
        title_xpath = x.select('//p[@class="titulo_iniciativa"]/text()')
        item = items.InitiativeItem()

        if title_xpath:
            record = title_xpath.re('(\d+/\d+)').pop()
            item['record'] = record
            title = title_xpath.pop().extract()

            initiative_type = x.select('//p[@class="subtitulo_competencias"]/text()').pop().extract()
            dates = x.select('//div[@class="resultados"]/div[@class="ficha_iniciativa"]/p[@class="texto"]/text()')

            register_date_re = dates.re('Presentado el \d{2}/\d{2}/\d{4}')
            register_date = dparser.parse(register_date_re.pop(), fuzzy=True).date() if register_date_re else None
            calification_date_re = dates.re('calificado el \d{2}/\d{2}/\{4}')
            calification_date = dparser.parse(calification_date_re.pop(), fuzzy=True).date() if register_date_re else None


            item['title'] = title
            item['term'] = ACTUAL_TERM
            item['register_date'] = register_date
            item['calification_date'] = calification_date
            item['initiative_type'] = initiative_type
            try:
                old_initiative = Initiative.objects.get(record=record)
            except:
                old_initiative = None

            initiative = item.save()

            if old_initiative != initiative:
                check_alert.delay(initiative)

            author_dip_re = x.select('//div[@id="RESULTADOS_BUSQUEDA"]/div[@class="resultados"]/div[@class="ficha_iniciativa"]/p[@class="texto"]/a').re('idDiputado=\d+')
            for author_dip in author_dip_re:
                author_dip_id = re.sub('idDiputado=', '', author_dip)
                member = Member.objects.get(congress_id__exact=author_dip_id)
                member.initiative_set.add(initiative)
                member.save()

            author_group_re = x.select('//div[@id="RESULTADOS_BUSQUEDA"]/div[@class="resultados"]/div[@class="ficha_iniciativa"]/p[@class="texto"]/a').re('idGrupo=\d+')
            for author_group in author_group_re:
                author_group_id = re.sub('idGrupo=', '', author_group)
                group = Group.objects.get(congress_id__exact=author_group_id)
                group.initiative_set.add(initiative)
                group.save()

            html = BeautifulSoup(response.body)

            commissions_html = html.findAll(lambda tag: tag.name == 'a' and\
                                            tag.findParent('div',\
                                            attrs={'class':'ficha_iniciativa'})\
                                            and tag.findChildren('b',\
                                            text=re.compile("Comisi")))
            for commission_html in commissions_html:
                commission_url = commission_html.attrs['href']
                query = urlparse.parse_qs(urlparse.urlparse(commission_url).query)
                congress_id = query['idOrgano'][0]
                commission, created = Commission.objects.get_or_create(congress_id=congress_id, term=ACTUAL_TERM)
                commission.initiative_set.add(initiative)
                commission.congress_url = commission_url
                commission.name = commission_html.text
                commission.save()

        return item
