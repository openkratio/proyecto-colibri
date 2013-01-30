# -*- coding: utf-8 -*-
from scraping.views import scrap_group, scrap_groups
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        #scrap_groups()
        print "TODO"
