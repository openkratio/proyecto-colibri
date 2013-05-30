from tastypie.resources import ModelResource
from tastypie import fields

from common.api import BaseCorsResource
from parliamentarygroup.models import Group, GroupMember

class GroupResource(ModelResource, BaseCorsResource):
    members = fields.ToManyField('parliamentarygroup.api.GroupMemberResource',
                                 'groupmember_set',
                                 related_name='member',
                                 full=True)
    class Meta:
        queryset = Group.objects.all()
        allowed_methods = ['get']
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }
        resource_name = "group"

class GroupMemberResource(ModelResource, BaseCorsResource):
    member = fields.ToOneField('member.api.MemberResource',
                               'member',
                               full=True)

    class Meta:
        queryset = GroupMember.objects.all()
        allowed_methods = ['get']
        resource_name = "GroupMember"
        exclude = ['id']
