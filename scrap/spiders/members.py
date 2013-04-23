# coding=utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

import scrap.items as items


class MemberSpider(CrawlSpider):
    name = 'members'
    allowed_domains = ['congreso.es', ]
    start_urls = [
        'http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DiputadosLegFechas', ]
    rules = [
        Rule(SgmlLinkExtractor(
            allow=['/wc/fichaDiputado&idDiputado=\d+']), 'parse_member'),
        Rule(SgmlLinkExtractor(
            allow=['/wc/diputadosLegsFechas&paginaActual=\d+']), follow=True)]

    def parse_member(self, response):
        x = HtmlXPathSelector(response)

        item = items.MemberItem()

        item['congress_web'] = response.url
        #query = urlparse.parse_qs(urlparse.urlparse(response.url).query)
        #item['id_diputado'] = query['idDiputado']

        # extract full name of member
        names = x.select(
            '//div[@class="nombre_dip"]/text()').extract()
        # extra text like member's state
        curriculum = x.select(
            '//div[@class="texto_dip"]/ul/li/div[@class="dip_rojo"]')

        # email, twitter ....
        extra_data = x.select(
            '//div[@class="webperso_dip"]/div/a/@href')

        avatar = x.select(
            '//div[@id="datos_diputado"]/p[@class="logo_grupo"]/img[@name="foto"]/@src').extract()

        party_avatar = x.select(
            '//div[@id="datos_diputado"]/p[@class="logo_grupo"]/a/img/@src').extract()
        party_name = x.select(
            '//div[@id="datos_diputado"]/p[@class="nombre_grupo"]/text()').extract()

        party_avatar = party_avatar and party_avatar[0] or None
        party_name = party_name and party_name[0] or None

        if names:
            second_name, name = names[0].strip().split(',')
            item['name'] = name.encode('utf-8')
            item['second_name'] = second_name.encode('utf-8')
            if avatar:
                item['avatar'] = 'http://www.congreso.es' + avatar[0]
            if curriculum:
                state = curriculum.re('(?<=Diputad[ao] por)[\s]*[\w\s]*')
                if state:
                    item['division'] = state[0].strip()
                group = curriculum.select('a')
                if group:
                    group_url = group.select('@href').extract()
                    # url is in list, extract it
                    group_url = group_url and group_url[0] or None
                    # get group name and group term
                    # (e.g: G.P. Vasco (EAJ-PNV) ( GV (EAJ-PNV) )
                    group_name, group_term = group.re(
                        '(?P<name>G\.P\.[\w\s]* [\(\w\-\)]+)[\s]*\((?P<init>[\w\s\-]*)\)')
                    # TODO: store group
                    # TODO store party
            if extra_data:
                email = extra_data.re(
                    'mailto:[\w.-_]*@[\w.-_]*')
                if email:
                    item['email'] = email[0].replace('mailto:', '')
                twitter = extra_data.re(
                    '[http|https]*://(?:twitter.com)/[\w]*')
                if twitter:
                    item['twitter'] = twitter[0]

            person = item.save()  # save() return django's model class
        return item
