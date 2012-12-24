from django.db import models
from django.utils.translation import ugettext_lazy as _
from member.models import Member
from datetime import datetime

class Voting(models.Model):
    session = models.IntegerField(verbose_name=_("Session"), default=0, null=False)
    number = models.IntegerField(verbose_name=_("Number"), default=0, null=False)
    date = models.DateField(verbose_name=_("Date"), default=datetime.now(), null=False)
    title = models.CharField(max_length=255, verbose_name=_("Title"), null=False, default=_("Empty"))
    record_text = models.TextField(verbose_name=_("Record text"), null=False, default=_("Empty"))
    subgroup_title = models.CharField(max_length=255, verbose_name=_("Subgroup title"), null=False, default=_("Empty"))
    subgroup_text = models.TextField(verbose_name=_("Subgroup text"), null=False, default=_("Empty"))
    assent = models.BooleanField(verbose_name=_("Assent"), null=False, default=False)
    attendee = models.IntegerField(verbose_name=_("Attendee"), null=False, default=0)
    for_votes = models.IntegerField(verbose_name=_("For votes"), null=False, default=0)
    against_votes = models.IntegerField(verbose_name=_("Agaist votes"), null=False, default=0)
    abstains = models.IntegerField(verbose_name=_("Abstains"), null=False, default=0)
    no_votes = models.IntegerField(verbose_name=_("No votes"), null=False, default=0)

    class Meta:
        verbose_name = _("Voting")
        verbose_name_plural = _("Votings")

    def __unicode__(self):
        return u'%s, %s: %s (%s)' % (unicode(self.session), unicode(self.number), unicode(self.title), unicode(self.date))

class Vote(models.Model):
    member = models.ForeignKey(Member, verbose_name=_("Member"), default=None)
    voting = models.ForeignKey("Voting", verbose_name=_("Voting"), default=None)
    vote = models.CharField(max_length=20, verbose_name=_("Vote"), default=_("Empty"), null=False)

    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")

    def __unicode__(self):
        return u'%s, %s: %s' % (unicode(self.member), unicode(self.voting), unicode(self.vote))
