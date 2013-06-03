# coding=utf-8

from tastypie.resources import ModelResource
from tastypie import fields
from parliamentarygroup.models import Group, GroupMember


class GroupResource(ModelResource):
    members = fields.ToManyField(
        'member.api.MemberResource',
        attribute='members', related_name='member', full=True)

    class Meta:
        queryset = Group.objects.all().prefetch_related('members')
        resource_name = "group"
        allowed_methods = ['get']
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }


class GroupMemberResource(ModelResource):
    member = fields.ToOneField(
        'member.api.MemberResource', 'member', full=True)

    class Meta:
        queryset = GroupMember.objects.all().select_related('party', 'member')
        allowed_methods = ['get']
        resource_name = "GroupMember"
        exclude = ['id']
