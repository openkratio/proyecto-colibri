# coding=utf-8

import urlparse
import dateutil
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

import scrap.items as items

from parliamentarygroup.models import Group, Party, GroupMember
from term.models import Term


class MemberSpider(CrawlSpider):
    name = 'members'
    allowed_domains = ['congreso.es', ]


    def __init__(self, *args, **kwargs):
        self.rules = []
        term = kwargs.get('term')

        self.actual_term = Term.objects.latest('decimal') if not term else\
                           Term.objects.get(decimal=term)

        self.start_urls = ['http://www.congreso.es/portal/page/portal/Congreso'
                           '/Congreso/Diputados?_piref73_1333056_73_1333049_13'
                           '33049.next_page=/wc/menuAbecedarioInicio&tipoBusqu'
                           'eda=completo&idLegislatura=' +
                           str(self.actual_term.decimal), ]
        self.rules.append(
            Rule(SgmlLinkExtractor(
                allow=['fichaDiputado\?idDiputado=\d+&idLegislatura=' +
                       str(self.actual_term.decimal)], unique=True),
                       'parse_member'))
        self.rules.append(
            Rule(SgmlLinkExtractor(
                allow=['busquedaAlfabeticaDiputados&paginaActual=\d+&idLeg'
                       'islatura=' + str(self.actual_term.decimal) +
                       '&tipoBusqueda=completo'], unique=True), follow=True))

        super(MemberSpider, self).__init__(*args, **kwargs)

    def parse_member(self, response):
        x = HtmlXPathSelector(response)

        item = items.MemberItem()
        query = urlparse.parse_qs(urlparse.urlparse(response.url).query)
        item['congress_id'] = query['_piref73_1333155_73_1333154_1333154.next_'
                                    'page'][0].split('=')[1]
        item['congress_web'] = response.url

        # extract full name of member
        names = x.select('//div[@class="nombre_dip"]/text()').extract()
        # extra text like member's state
        curriculum = x.select('//div[@class="texto_dip"]/ul/li/div[@class="dip'
                              '_rojo"]')

        # email, twitter ....
        extra_data = x.select('//div[@class="webperso_dip"]/div/a/@href')
        avatar = x.select('//div[@id="datos_diputado"]/p[@class="logo_g'
                          'rupo"]/img[@name="foto"]/@src').extract()

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
                    group_list = group.re('(?P<name>[\w\s\-]*) '
                                          '\((?P<init>[\w\s\-]*)\)')
                    group_name = group_list[0]
                    group_term = ''.join(group_list[1:])

                    if group_url:
                        group_congress_id = urlparse.parse_qs\
                                            (group_url)['idGrupo'].pop()
                        group_instance, created_group = Group.objects.\
                                get_or_create(congress_id=group_congress_id,
                                              term=self.actual_term)
                        group.congress_url = group_url
                        group_instance.name = group_name
                        group_instance.acronym = group_term

                        group_instance.term = self.actual_term
                        group_instance.save()

                    party_avatar = x.select('//div[@id="datos_diputado"]/p[@cl'
                                            'ass="logo_grupo"]/a/img/@src').\
                                            extract()
                    party_name = x.select('//div[@id="datos_diputado"]/p[@clas'
                                          's="nombre_grupo"]/text()').extract()

                    party_avatar = party_avatar and party_avatar[0] or None
                    party_name = party_name and party_name[0] or None

                    if party_name:
                        party_instance, created_party = Party.objects.\
                                                get_or_create(name=party_name)
                        party_instance.logo = party_avatar
                        party_instance.save()
                    # add dates of inscription and termination
                    ins_date = curriculum.re('(?i)(?<=fecha alta:)[\s]*[\d\/]*')
                    if ins_date:
                        item['inscription_date'] = dateutil.parser.parse\
                                                   (ins_date[0], dayfirst=True)
                    term_date = curriculum.re('(?i)(?<=caus\xf3 baja el)[\s]*['
                                              '\d\/]*')
                    if term_date:
                        item['termination_date'] = dateutil.parser.parse\
                                                   (term_date[0], dayfirst=True)

            if extra_data:
                web_data = x.select('//div[@class="webperso_dip"]/div[@class="'
                                    'webperso_dip_parte"]/a/@href')
                if web_data:
                    web = web_data.re('[http|https]*://.*')
                    if web:
                        item['web'] = web[0]
                email = extra_data.re('mailto:[\w.-_]*@[\w.-_]*')
                if email:
                    item['email'] = email[0].replace('mailto:', '')
                twitter = extra_data.re('[http|https]*://(?:twitter.com)/[\w]*')
                if twitter:
                    item['twitter'] = twitter[0]

            member_instance = item.save()  # save() return django's model class

            gm_instance, creatd_gm = GroupMember.objects.get_or_create\
                                              (group = group_instance,
                                              member = member_instance,
                                              party = party_instance)
            gm_instance.save()

        return item
