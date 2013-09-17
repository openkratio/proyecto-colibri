# coding=utf-8
from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS, ALL

from initiatives.models import Initiative
from main.api import ColibriResource


class InitiativeResource(ColibriResource):
    authors = fields.ToManyField('member.api.MemberResource', 'author', full=True)
    authors_group = fields.ToManyField('parliamentarygroup.api.GroupResource', 'author_group', full=True)

    class Meta:
        resource_name = "initiative"
        queryset = Initiative.objects.all().select_related('author', 'author_group')
        allowed_methods = ['get']
        filtering = {
                "authors": ALL_WITH_RELATIONS,
                "authors_group": ALL_WITH_RELATIONS,
                "calification_date": ALL,
                "id": ALL,
                "initiative_type": ALL,
                "record": ALL,
                "register_date": ALL,
                "resource_uri": ALL,
                "title": ALL,

        }
