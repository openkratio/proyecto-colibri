# coding=utf-8
import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

import scrap.items as items

from parliamentarygroup.models import Group, Party, GroupMember
from term.models import Term

actual_term = Term.objects.latest('id')

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
        query = urlparse.parse_qs(urlparse.urlparse(response.url).query)
        item['congress_id'] = query['idDiputado'][0]

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

        if names:
            second_name, name = names[0].split(',')
            item['name'] = name.strip().encode('utf-8')
            item['second_name'] = second_name.strip().encode('utf-8')
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
                    # get group name (<name> and group term <init>
                    # (e.g: G.P. Vasco (EAJ-PNV) ( GV (EAJ-PNV) )
                    group_name, group_term = group.re(
                        '(?P<name>G\.P\.[\w\s]* [\(\w\-\)]+)[\s]*\((?P<init>[\w\s\-]*)\)')
                    # TODO: store group
                    if group_url:
                        group_instance, created_group = Group.objects.get_or_create(congress_url=group_url,
                                                                                    term=actual_term)
                        group_instance.name = group_name
                        group_instance.acronym = group_term

                        group_instance.term = actual_term
                        group_instance.congress_id = urlparse.parse_qs(group_url)['idGrupo'].pop()
                        group_instance.save()

                    # TODO store party
                    party_avatar = x.select(
                        '//div[@id="datos_diputado"]/p[@class="logo_grupo"]/a/img/@src').extract()
                    party_name = x.select(
                        '//div[@id="datos_diputado"]/p[@class="nombre_grupo"]/text()').extract()

                    party_avatar = party_avatar and party_avatar[0] or None
                    party_name = party_name and party_name[0] or None

                    if party_name:
                        party_instance, created_party = Party.objects.get_or_create(name=party_name)
                        party_instance.logo = party_avatar
                        party_instance.save()



            if extra_data:
                web_data = x.select(
                    '//div[@class="webperso_dip"]/div[@class="webperso_dip_parte"]/a/@href')
                if web_data:
                    web = web_data.re('[http|https]*://.*')
                    if web:
                        item['web'] = web[0]
                email = extra_data.re(
                    'mailto:[\w.-_]*@[\w.-_]*')
                if email:
                    item['email'] = email[0].replace('mailto:', '')
                twitter = extra_data.re(
                    '[http|https]*://(?:twitter.com)/[\w]*')
                if twitter:
                    item['twitter'] = twitter[0]

            member_instance = item.save()  # save() return django's model class

            gm_instance, creatd_gm = GroupMember.objects.get_or_create(group = group_instance,
                                              member = member_instance,
                                              party = party_instance)
            gm_instance.save()

        return item
