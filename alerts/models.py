#coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Alert(models.Model):
    user = models.ForeignKey(User)
    key_words = models.CharField(_("Key words"), max_length=255, null=False,
                                 blank=False, default="None")

    class Meta:
        verbose_name = _("Alert")
        verbose_name_plural = _("Alerts")

    def __unicode__(self):
        return u'%s: %s' % (self.user, self.key_words)

class SendedAlert(models.Model):
    alert = models.ForeignKey(Alert)
    sended = models.DateTimeField(auto_now_add=True)
    is_ok = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Sended Alert")
        verbose_name_plural = _("Sended Alerts")

    def __unicode__(self):
        return u'%s: %s' % (self.alert, self.sended)
