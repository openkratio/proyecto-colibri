# Scrapy settings for scrap project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import imp
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colibri.settings")
from django.conf import settings

BOT_NAME = 'colibri'

SPIDER_MODULES = ['scrap.spiders']
NEWSPIDER_MODULE = 'scrap.spiders'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib_exp.downloadermiddleware.decompression.DecompressionMiddleware': None
}

DOWNLOAD_DELAY = 0.5
