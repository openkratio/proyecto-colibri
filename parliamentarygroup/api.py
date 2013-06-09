from tastypie.resources import ModelResource
from tastypie import fields

from parliamentarygroup.models import Group, GroupMember, Party

class GroupManagerResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        allowed_methods = ['get']
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }


class GroupResource(GroupManagerResource):
    members = fields.ToManyField('parliamentarygroup.api.GroupMemberResource',
                                 'groupmember_set',
                                 related_name='member',
                                 full=True)

    class Meta(GroupManagerResource.Meta):
        resource_name = "group"

class PartyResource(ModelResource):
    class Meta:
        queryset = Party.objects.all()
        allowed_methods = ['get']
        resource_name = 'party'
        limit = 0

class GroupMemberResource(ModelResource):
    member = fields.ToOneField('member.api.MemberResource',
                               'member',
                               full=True)

    party = fields.ToOneField('parliamentarygroup.api.PartyResource',
                               'party')
    class Meta:
        queryset = GroupMember.objects.all()
        allowed_methods = ['get']
        resource_name = "GroupMember"
        exclude = ['id']
