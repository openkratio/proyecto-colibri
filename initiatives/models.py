#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from commission.models import Commission
from member.models import Member
from parliamentarygroup.models import Group
from term.models import Term
from vote.models import Voting


class Initiative(models.Model):
    term = models.ForeignKey(Term)
    initiative_type = models.CharField(max_length=150, verbose_name=_("Initiative type"), null=True)
    record = models.CharField(max_length=25, verbose_name=_("Record code"))
    register_date = models.DateField(verbose_name=_("Presentation date"), null=True)
    calification_date = models.DateField(verbose_name=_("Calification date"), null=True)
    author = models.ManyToManyField(Member)
    author_group = models.ManyToManyField(Group)
    comissions = models.ManyToManyField(Commission)
    votings = models.ManyToManyField(Voting)
    title = models.TextField(verbose_name=_("Title"), null=True)
    url = models.URLField(max_length=500, default="")

    class Meta:
        verbose_name = _("Initiative")
        verbose_name_plural = _("Initiatives")

    def __unicode__(self):
        return u'%s' % (self.record)

