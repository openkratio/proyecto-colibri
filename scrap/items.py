# coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.contrib_exp.djangoitem import DjangoItem
import member.models as members


class MemberItem(DjangoItem):
    django_model = members.Member
