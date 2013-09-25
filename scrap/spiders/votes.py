# coding=utf-8

from dateutil import parser as date_parser
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from scrapy import log
from scrapy.http import Request

from bs4 import BeautifulSoup
import datetime
import re

from initiatives.models import Initiative
from member.models import Member
from vote.models import Session, Voting, Vote


class VotesSpider(CrawlSpider):
    name = 'votes'
    allowed_domains = ['congreso.es']
    host = "http://www." + allowed_domains[0]


    def __init__(self, *args, **kwargs):
        self.rules = [
        ]

        date_session = kwargs.get('date')

        if date_session:
            self.start_urls = ['http://www.congreso.es/portal/page/portal/Congreso/Congreso/Actualidad/Votaciones?_piref73_9564074_73_9536063_9536063.next_page=/wc/accesoHistoricoVotaciones&fechaSeleccionada=' + date_session,]
            self.rules.append(
                Rule(
                    SgmlLinkExtractor(
                        deny=[
                            '/wc/accesoHistoricoVotaciones&fechaSeleccionada=\d+/\d+/iz',
                            '/wc/accesoHistoricoVotaciones&fechaSeleccionada=\d+/\d+/de',],
                        allow=['/wc/accesoHistoricoVotaciones&fechaSeleccionada=' + date_session]),
                    callback='parse_voting')
            )
        else:
            self.start_urls = [
                'http://www.congreso.es/portal/page/portal/Congreso/Congreso/Actualidad/Votaciones/',
            ]

            now = datetime.datetime.now()
            date_session = now.strftime('%Y/%m/')

            self.rules.append(
                Rule(
                SgmlLinkExtractor(
                    deny=[
                        '/wc/accesoHistoricoVotaciones&fechaSeleccionada=\d+/\d+/de',
                        ],
                    allow=[
                        '/wc/accesoHistoricoVotaciones&fechaSeleccionada=\d+/\d+/iz',
                        '/wc/accesoHistoricoVotaciones&fechaSeleccionada=\d+/\d+/\d+'],
                    unique=True),
                follow=True, callback='parse_voting')
            )

        super(VotesSpider, self).__init__(*args, **kwargs)

    def parse_voting(self, response):
        html = BeautifulSoup(response.body)
        links = html.findAll('a', attrs={"style":"font-weight:bold"})

        for link in links:
            votings = []
            if link.parent.attrs.has_key('onclick'):
                single_voting = re.search('\d+,\d+,\d+,\d+', link.parent.attrs['onclick'], re.M|re.I)
            else:
                single_voting = None

            if single_voting:
                data = single_voting.group(0).split(',')
                votings = [html.find('a', href=re.compile('/votaciones/OpenData\?sesion={0}&votacion={1}&legislatura={2}'.format(data[0], data[1], data[2])))]
            else:
                votings = link.parent.findChildren('a', href=re.compile('/votaciones/OpenData\?sesion=\d+&votacion=\d+&legislatura=\d+'))
                if not votings:
                    votings = link.parent.parent.findChildren('a', href=re.compile('/votaciones/OpenData\?sesion=\d+&votacion=\d+&legislatura=\d+'))

            for voting in votings:
                record = re.sub('\(N\\xfam. expte. ', '', link.text).strip(')')
                href="{0}{1}".format(self.host, voting.attrs['href'])
                voting =  Request(href, callback=self.parse_vote)
                voting.meta['record'] = record
                yield voting

    def parse_vote(self, response):
        if not hasattr(response, 'body_as_unicode'):
            self.log(
                'Cannot parse: {u}'.format(u=response.url), level=log.INFO)
            return
        x = XmlXPathSelector(response)

        info = x.select('//Resultado/Informacion')
        session_id = info.select('//Sesion/text()').extract()
        if not session_id:
            # can't identify session, so we skip this file
            self.log(
                'Missing session ID: {u}'.format(u=response.url),
                level=log.INFO)
            return
        # general session info
        session_id = session_id[0]
        session_date = date_parser.parse(
            info.select('//Fecha/text()').extract()[0], dayfirst=True)
        session_instance, session_created = Session.objects.get_or_create(
            session=session_id, defaults={'date': session_date})
        if not session_created:
            session_instance.date = session_date
            session_instance.save()

        # specific voting session info
        voting_number = info.select('//NumeroVotacion/text()').extract()
        if not voting_number:
            self.log(
                'Missing voting number: {u}'.format(u=response.url),
                level=log.INFO)
            return
        voting_number = voting_number[0]
        voting_title = info.select('//Titulo/text()').extract()[0]
        voting_text = info.select('//TextoExpediente/text()').extract()[0]
        voting_title_sub = info.select('//TituloSubGrupo/text()').extract()
        voting_title_sub = voting_title_sub[0] if voting_title_sub else ''
        voting_text_sub = info.select('//TextoSubGrupo/text()').extract()
        voting_text_sub = voting_text_sub[0] if voting_text_sub else ''

        voting_instance, voting_created = Voting.objects.get_or_create(
            session=session_instance, number=voting_number)
        voting_instance.title = voting_title
        voting_instance.record_text = voting_text
        voting_instance.subgroup_title = voting_title_sub
        voting_instance.subgroup_text = voting_text_sub
        # voting session counters
        counts = x.select('//Resultado/Totales')
        counts_assent = counts.select('//Asentimiento/text()').extract()[0]
        if counts_assent.lower() == 'no':
            counts_assent = False
        else:
            counts_assent = True
        if counts_assent is False:
            counts_presents = counts.select('//Presentes/text()').extract()[0]
            counts_for = counts.select('//AFavor/text()').extract()[0]
            counts_against = counts.select('//EnContra/text()').extract()[0]
            counts_abstentions = counts.select(
                '//Abstenciones/text()').extract()[0]
            counts_dont = counts.select('//NoVotan/text()').extract()[0]

            voting_instance.attendee = counts_presents
            voting_instance.for_votes = counts_for
            voting_instance.against_votes = counts_against
            voting_instance.abstains = counts_abstentions
            voting_instance.no_votes = counts_dont

        voting_instance.assent = counts_assent

        record = response.meta['record']
        initiatives = Initiative.objects.filter(record__exact=record)
        if initiatives:
            voting_instance.votings.add(initiatives.latest('id'))

        voting_instance.save()

        if counts_assent is False:
            # time to parse votes!
            votes = x.select('//Resultado/Votaciones/Votacion')
            Vote.objects.filter(voting=voting_instance).delete()
            votes_list = []
            for v in votes:
                member_seat = v.select('Asiento/text()').extract()[0]
                # @jneight: I don't like search members by name, seats better?
                full_name = v.select('Diputado/text()').extract()[0]
                second_name, first_name = full_name.split(',')
                vote_type = v.select('Voto/text()').extract()[0]
                member_pk = Member.objects.filter(
                    name__iexact=first_name.strip(),
                    second_name__iexact=second_name.strip()
                ).values_list('pk', flat=True)
                if member_pk:
                    votes_list.append(Vote(
                        voting=voting_instance, member_id=member_pk[0],
                        vote=vote_type))
            Vote.objects.bulk_create(votes_list)

        return voting_instance

    def parse_session(self, response):
        """
            Get the HTML with descriptions and other stuff
        """
        x = HtmlXPathSelector(response)
