from django.db import models
from django.utils.translation import ugettext_lazy as _

from term.models import Term

from member.models import Member

class Party(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    logo = models.ImageField(upload_to='images/logos/parties',
                             verbose_name=_("Logo"),
                             null=True)
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
    members = models.ManyToManyField(Member, through='GroupMember')

    class Meta:
        verbose_name = _("Parlamentary Group")
        verbose_name_plural = _("Parlamentaries Groups")

    def __unicode__(self):
        return u'%s' % (unicode(self.name))

class GroupMember(models.Model):
    group = models.ForeignKey(Group, verbose_name='Group')
    member = models.ForeignKey(Member, verbose_name='Member')
    party = models.ForeignKey(Party, verbose_name='Party', null=True)
