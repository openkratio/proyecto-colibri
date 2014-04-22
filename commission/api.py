# coding=utf-8
from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.resources import ALL

from commission.models import Commission
from main.api import ColibriResource


class CommissionManagerResource(ColibriResource):
    term = fields.IntegerField(attribute='term__decimal',
                               readonly=True, null=True)
    class Meta:
        resource_name = "commission"
        queryset = Commission.objects.all()
        allowed_methods = ['get']
        filtering = {
                "name": ALL,
                "id": ALL,
                "congress_url": ALL,
                "congress_id": ALL,
                "term": ('exact',),
        }
        cache = SimpleCache(timeout=1440)
