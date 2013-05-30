from tastypie.resources import ModelResource

from common.api import BaseCorsResource
from member.models import Member

class MemberResource(ModelResource, BaseCorsResource):
    class Meta:
        queryset = Member.objects.all()
        allowed_methods = ['get']
        resource_name = "member"

        filtering = {
            "name": ('exact','startswith','iexact','istartswith',),
            "id": ('exact',),
        }
