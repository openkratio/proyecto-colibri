from django.db import models
from django.utils.translation import ugettext_lazy as _
from term.models import Term

# Create your models here.
class Party(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    logo = models.ImageField(upload_to='images/logos/parties', verbose_name=_("Logo"), null=True)
    web = models.URLField(verbose_name=_("Web"), null=True)
    validate = models.BooleanField(default=True, verbose_name=_("Validate"))

    class Meta:
        verbose_name = _("Party")
        verbose_name_plural = _("Parties")

    def __unicode__(self):
        return u'%s' % (unicode(self.name))

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    acronym = models.CharField(max_length=10, verbose_name=_("Acronym"), null=True)
    term = models.ForeignKey(Term, verbose_name=_("Term"))
    congress_url = models.URLField(verbose_name=_("Congress url"), null=True)
    validate = models.BooleanField(default=True, verbose_name=_("Validate"))
    parties = models.ManyToManyField(Party, through='GroupParty')

    class Meta:
        verbose_name = _("Parlamentary Group")
        verbose_name_plural = _("Parlamentaries Groups")

    def __unicode__(self):
        return u'%s' % (unicode(self.name))

class GroupParty(models.Model):
    group = models.ForeignKey('Group', verbose_name=_("Group"))
    party = models.ForeignKey('Party', verbose_name=_("Party"))

    class Meta:
        verbose_name = _("Party in group")
        verbose_name_plural = _("Parties in groups")

    def __unicode__(self):
        return u'%s, %s' % (unicode(self.group), unicode(self.party))

class Color(models.Model):
    name = models.CharField(max_length=50, default='#000000', null=False, verbose_name=_("Color"))
    party = models.ForeignKey('Party', verbose_name=_("Party"))

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __unicode__(self):
        return u'%s' % (unicode(self.name))
