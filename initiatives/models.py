#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from member.models import Member
from term.models import Term


class Initiative(models.Model):
    term = models.ForeignKey(Term)
    initiative_type = models.CharField(max_length=150, verbose_name=_("Initiative type"), null=True)
    record = models.CharField(max_length=25, verbose_name=_("Record code"))
    register_date = models.DateField(verbose_name=_("Presentation date"), null=True)
    calification_date = models.DateField(verbose_name=_("Calification date"), null=True)
    #author = models.ManyToManyField(Member)
    #author_text = models.CharField(max_length=100,\
    #                               verbose_name=_("Author text"))
    title = models.CharField(max_length=255, verbose_name=_("Title"), null=True)
    #tramitation_type = models.CharField(max_length=100,\
    #                                    verbose_name=_("Tramitation type"))
    #commissions =
    #periods =
    #processings
    #boes


class Status(models.Model):
    follow = models.CharField(max_length=150, verbose_name=_("Initiative follow by"))
    start_date = models.DateField(verbose_name=_("Start date"))
    end_date = models.DateField(verbose_name=_("End date"))
    initiative = models.ForeignKey(Initiative)

    class Meta:
        verbose_name = _("Status initiative")
        verbose_name_plural = _("Status initiatives")

    def __unicode__(self):
        return u'%d' % (self.follow)

