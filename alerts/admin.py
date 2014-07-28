#coding=utf-8
from django.contrib import admin

from alerts.models import Alert, SendedAlert

admin.site.register(Alert)
admin.site.register(SendedAlert)
