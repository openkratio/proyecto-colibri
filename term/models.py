from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime


class Term(models.Model):
    roman = models.CharField(max_length=10, verbose_name=_("Roman"))
    decimal = models.IntegerField(verbose_name=_("Decimal"))
    start_date = models.DateField(verbose_name=_("Start date"),
                                  null=False,
                                  default=datetime.now().date())
    end_date = models.DateField(verbose_name=_("End date"),
                                null=False,
                                blank=True,
                                default=datetime.now().date())

    class Meta:
        verbose_name = _("Term")
        verbose_name_plural = _("Terms")

    def __unicode__(self):
        return u'%s' % (unicode(self.roman))
