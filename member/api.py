# coding=utf-8
from tastypie.cache import SimpleCache

from main.api import ColibriResource
from member.models import Member


class MemberResource(ColibriResource):
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
        cache = SimpleCache(cache_name='default', timeout=1440)
