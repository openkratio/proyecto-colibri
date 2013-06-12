# coding=utf-8

from tastypie.resources import ModelResource
from tastypie import fields
from main.fields import OptimizedToOneField

from parliamentarygroup.models import Group, GroupMember, Party


class GroupManagerResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        allowed_methods = ['get']


class GroupResource(GroupManagerResource):
    members = fields.ToManyField(
        'parliamentarygroup.api.GroupMemberResource',
        lambda bundle: bundle.obj.members.through.objects.filter(
            group=bundle.obj.pk).select_related('member') or
        bundle.obj.members, related_name='members_set', full=True)

    class Meta(GroupManagerResource.Meta):
        queryset = Group.objects.all()
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }
        resource_name = "group"


class GroupMemberResource(ModelResource):
    member = fields.ToOneField(
        'member.api.MemberResource', 'member', full=True)
    party = OptimizedToOneField(
        'parliamentarygroup.api.PartyResource', 'party', null=True)

    class Meta:
        queryset = GroupMember.objects.all().select_related('member')
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
