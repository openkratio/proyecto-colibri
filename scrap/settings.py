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

BOT_NAME = 'colibri'

SPIDER_MODULES = ['scrap.spiders']
NEWSPIDER_MODULE = 'scrap.spiders'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib_exp.downloadermiddleware.decompression.DecompressionMiddleware': None
}

DOWNLOAD_DELAY = 0.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrap (+http://www.yourdomain.com)'


def setup_django_env(path):
    f, filename, desc = imp.find_module('settings', [path])
    project = imp.load_module('settings', f, filename, desc)

    setup_environ(project)

    # Add django project to sys.path
    sys.path.append(os.path.abspath(os.path.join(path, os.path.pardir)))

# setup_django_env('colibri/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colibri.settings")
