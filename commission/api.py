# coding=utf-8
from tastypie.resources import ALL

from commission.models import Commission
from main.api import ColibriResource


class CommissionManagerResource(ColibriResource):
    class Meta:
        resource_name = "commission"
        queryset = Commission.objects.all()
        allowed_methods = ['get']
        filtering = {
                "name": ALL,
                "id": ALL,
                "congress_url": ALL,
                "congress_id": ALL,
        }
