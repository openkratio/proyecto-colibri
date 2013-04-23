# coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.contrib_exp.djangoitem import DjangoItem
import member.models as members
import parliamentarygroup.models as pg


class MemberItem(DjangoItem):
    django_model = members.Member


class GroupItem(DjangoItem):
    django_model = pg.Group


class PartyItem(DjangoItem):
    django_model = pg.Party
