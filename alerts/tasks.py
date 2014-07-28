# coding=utf-8
from __future__ import absolute_import
from datetime import datetime, timedelta
import re
import time

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from alerts.models import Alert, SendedAlert


def send_alert(initiative, alert):
    sended_alert = SendedAlert(alert=alert)
    sended_alert.save()

    one_hour_ago = sended_alert.sended - timedelta(minutes=settings.TIME_QUOTE)
    sended_hour_ago = SendedAlert.objects.filter(sended__gt=one_hour_ago).\
        order_by('sended')

    if sended_hour_ago.count() >= settings.NUM_QUOTE:
        first_sended = sended_hour_ago.first()
        seconds_to_wait = (send_alert.sended - first_sended).seconds
        time.sleep(seconds_to_wait)
    try:
        msg = "%s\n%s" % (initiative.title, initiative.url)
        send_mail(alert.key_words, msg,
                  'alert@proyectocolibri.es',
                  [alert.user.email], fail_silently=False)
    except:
        send_alert.is_ok = False
        send_alert.save()

@shared_task
def check_alert(initiative):
    queryset_alerts = Alert.objects.all()
    alerts = [alert for alert in queryset_alerts
              if re.search(alert.key_words.replace(' ', '|'),
                           initiative.title)]
    for alert in alerts:
        send_alert(initiative, alert)
