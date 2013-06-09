# coding=utf-8
from tastypie.resources import ModelResource

from member.models import Member


class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.all()
        allowed_methods = ['get']
        resource_name = "member"
        filtering = {
            "name": ('exact', 'startswith', 'iexact', 'istartswith',),
            "second_name": ('exact', 'startswith', 'iexact', 'istartswith',),
            "id": ('exact',),
        }
        limit = 0
