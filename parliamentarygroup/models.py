from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    acronym = models.CharField(max_length=10, verbose_name=_("Acronym"))
    start_date = models.DateField(verbose_name=_("Start date"))
    end_date = models.DateField(verbose_name=_("End date"))
    term = models.IntegerField(verbose_name=_("Term"))
    validate = models.BooleanField(default=True, verbose_name=_("Validate"))

    class Meta:
        verbose_name = _("Parlamentary Group")
        verbose_name_plural = _("Parlamentaries Groups")

    def __unicode__(self):
        return u'%s' % (unicode(self.name))

class Party(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    logo = models.ImageField(upload_to='images/logos/parties', verbose_name=_("Logo"))
    web = models.URLField(verbose_name=_("Web"))
    group = models.ForeignKey('Group', verbose_name=_("Group"))
    validate = models.BooleanField(default=True, verbose_name=_("Validate"))

    class Meta:
        verbose_name = _("Party")
        verbose_name_plural = _("Parties")

    def __unicode__(self):
        return u'%s' % (unicode(self.name))

class Color(models.Model):
    name = models.CharField(max_length=50, default='#000000', null=False, verbose_name=_("Color"))
    party = models.ForeignKey('Party', verbose_name=_("Party"))

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __unicode__(self):
        return u'%s' % (unicode(self.name))
