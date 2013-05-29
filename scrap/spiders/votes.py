# coding=utf-8

from dateutil import parser as date_parser
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from scrapy import log

import scrap.items as items
from vote.models import Session, Voting, Vote
from member.models import Member


class VotesSpider(CrawlSpider):
    name = 'votes'
    allowed_domains = ['congreso.es']
    start_urls = [
        'http://www.congreso.es/portal/page/portal/Congreso/Congreso/Actualidad/Votaciones/',
    ]

    rules = [
        Rule(
            SgmlLinkExtractor(
                allow=['/votaciones/OpenData'], unique=True),
            callback='parse_vote'),
        Rule(
            SgmlLinkExtractor(
                allow=['/wc/accesoHistoricoVotaciones&fechaSeleccionada='],
                unique=True),
            follow=True, callback='parse_session')]

    def parse_vote(self, response):
        """
            Load the zip file with the XMLs

            can't use '/votaciones/OpenData?sesion=\d*&completa=1&legislatura=10'
            as regex rule
        """

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
            info.select('//Fecha/text()').extract()[0])
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
        voting_instance.save()

        if counts_assent is False:
            # time to parse votes!
            votes = x.select('//Votaciones')
            for v in votes:
                member_seat = v.select('//Asiento/text()').extract()[0]
                # @jneight: I don't like search members by name, seats better?
                full_name = v.select('//Diputado/text()').extract()[0]
                second_name, first_name = full_name.split(',')
                vote_type = v.select('//Voto/text()').extract()[0]
                member_pk = Member.objects.filter(
                    name__iexact=first_name.strip(),
                    second_name__iexact=second_name.strip()
                ).values_list('pk', flat=True)
                if member_pk:
                    vote_instance, vote_created = Vote.objects.get_or_create(
                        voting=voting_instance, member_id=member_pk[0],
                        defaults={'vote': vote_type})
                    if not vote_created:
                        vote_instance.vote = vote_type
                        vote_instance.save()

    def parse_session(self, response):
        """
            Get the HTML with descriptions and other stuff
        """
        x = HtmlXPathSelector(response)
