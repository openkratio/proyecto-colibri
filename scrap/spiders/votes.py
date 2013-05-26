# coding=utf-8

import urlparse
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector

import scrap.items as items


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
                allow=['/wc/accesoHistoricoVotaciones&fechaSeleccionada=']),
            follow=True, callback='parse_session')]

    def parse_vote(self, response):
        """
            Load the zip file with the XMLs

            can't use '/votaciones/OpenData?sesion=\d*&completa=1&legislatura=10'
            as regex rule
        """
        x = XmlXPathSelector(response)

    def parse_session(self, response):
        """
            Get the HTML with descriptions and other stuff
        """
        x = HtmlXPathSelector(response)