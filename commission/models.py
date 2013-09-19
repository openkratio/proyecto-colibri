#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from term.models import Term

class Commission(models.Model):
    term = models.ForeignKey(Term)
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    congress_url = models.URLField(verbose_name=_("Congress Url"))
    congress_id = models.CharField(max_length=10, verbose_name=_("Congress ID"))

    class Meta:
        verbose_name = _("Commission")
        verbose_name_plural = _("Commissions")

    def __unicode__(self):
        return u'%s' % (self.name)
