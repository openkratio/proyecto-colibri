from django.db import models
from django.utils.translation import ugettext_lazy as _
from parliamentarygroup.models import Party


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
    parties = models.ManyToManyField(Party, through='MemberParty')
    congress_id = models.CharField(
        max_length=32, verbose_name='Member ID in congress\' web', default='',
        unique=True)

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __unicode__(self):
        return u'%s, %s' % (unicode(self.name), unicode(self.second_name))


class Seat(models.Model):
    image = models.ImageField(
        upload_to='images/seats', verbose_name=_("Image"))
    number = models.IntegerField(
        verbose_name=_("Seat number"), null=False, default=0)

    class Meta:
        verbose_name = _("Seat")
        verbose_name_plural = _("Seat")

    def __unicode__(self):
        return u'%s' % (unicode(self.image))


class MemberParty(models.Model):
    party = models.ForeignKey(Party, verbose_name=("Party"))
    member = models.ForeignKey('Member', verbose_name=("Member"))
    seat = models.ForeignKey(
        'Seat', verbose_name=("Seat"), null=True, default=None)
    start_date = models.DateField(
        verbose_name=_("Start date"), null=True, default=None)
    end_date = models.DateField(
        verbose_name=_("End date"), null=True, default=None)

    class Meta:
        verbose_name = _("Member in party")
        verbose_name_plural = _("Members in parties")

    def __unicode__(self):
        return u'%s: %s' % (unicode(self.member), unicode(self.party))
