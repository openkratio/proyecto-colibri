# coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Member(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    second_name = models.CharField(max_length=50, verbose_name=("Second name"))
    avatar = models.URLField(verbose_name=_("Avatar"), null=True)
    congress_web = models.URLField(verbose_name=_("Congress web"))
    email = models.EmailField(verbose_name=("Email"))
    web = models.URLField(verbose_name=_("Web"))
    twitter = models.URLField(verbose_name=_("Twitter"))
    #TODO add city app
    division = models.CharField(max_length="50", verbose_name=_("Division"))
    validate = models.BooleanField(default=True, verbose_name=_("Validate"))
    congress_id = models.CharField(max_length=32,
                                   verbose_name='Member ID in congress\' web',
                                   default=0)

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __unicode__(self):
        return u'%s, %s' % (unicode(self.name), unicode(self.second_name))
