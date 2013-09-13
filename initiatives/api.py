# coding=utf-8
from initiatives.models import Initiative
from main.api import ColibriResource


class InitiativeResource(ColibriResource):
    class Meta:
        queryset = Initiative.objects.all()
        allowed_methods = ['get']
