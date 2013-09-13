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
    author = models.ManyToManyField(Member)
    title = models.CharField(max_length=255, verbose_name=_("Title"), null=True)

    class Meta:
        verbose_name = _("Initiative")
        verbose_name_plural = _("Initiatives")

    def __unicode__(self):
        return u'%s' % (self.record)

