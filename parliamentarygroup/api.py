# coding=utf-8

from tastypie.resources import ModelResource
from tastypie import fields

from parliamentarygroup.models import Group, GroupMember, Party

class GroupManagerResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        allowed_methods = ['get']


class GroupResource(GroupManagerResource):
    members = fields.ToManyField('parliamentarygroup.api.GroupMemberResource',
                                 'groupmember_set',
                                 related_name='member',
                                 full=True)

    class Meta(GroupManagerResource.Meta):
        queryset = Group.objects.all().prefetch_related('members')
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }
        resource_name = "group"


class GroupMemberResource(ModelResource):
    member = fields.ToOneField('member.api.MemberResource',
                               'member',
                               full=True)
    party = fields.ToOneField('parliamentarygroup.api.PartyResource',
                              'party',
                              null=True)

    party = fields.ToOneField('parliamentarygroup.api.PartyResource',
                               'party')
    class Meta:
        queryset = GroupMember.objects.all().select_related('party', 'member')
        allowed_methods = ['get']
        resource_name = "GroupMember"
        exclude = ['id']
        include_resource_uri = False

class PartyResource(ModelResource):
    class Meta:
        queryset = Party.objects.all()
        allowed_methods = ['get']
        resource_name = "party"
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }
