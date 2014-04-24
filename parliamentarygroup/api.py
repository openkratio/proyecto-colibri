# coding=utf-8
from tastypie import fields
from tastypie.cache import SimpleCache

from main.api import ColibriResource
from main.fields import OptimizedToOneField
from parliamentarygroup.models import Group, GroupMember, Party


class GroupManagerResource(ColibriResource):
    term = fields.IntegerField(attribute='term__decimal',
                               readonly=True, null=True)
    class Meta:
        queryset = Group.objects.all()
        allowed_methods = ['get']
        filtering = {
            "name": ('exact', 'startswith', 'iexact', 'istartswith',),
            "id": ('exact',),
        }
        resource_name = "simple_group"
        cache = SimpleCache(timeout=1440)


class GroupResource(GroupManagerResource):
    class Meta(GroupManagerResource.Meta):
        queryset = Group.objects.all()
        filtering = {
            "name": ('exact', 'startswith', 'iexact', 'istartswith',),
            "id": ('exact',),
            "term": ('exact',),
        }
        resource_name = "group"


class GroupMemberResource(ColibriResource):
    member = fields.ToOneField(
        'member.api.MemberResource', 'member', full=True)
    party = OptimizedToOneField(
        'parliamentarygroup.api.PartyResource', 'party', null=True)
    term = fields.IntegerField(attribute='group__term__decimal',
                               readonly=True, null=True)

    class Meta:
        queryset = GroupMember.objects.all().prefetch_related('member')
        allowed_methods = ['get']
        resource_name = "groupmember"
        filtering = {
            "term": ('exact',),
        }
        exclude = ['id']
        include_resource_uri = False
        cache = SimpleCache(timeout=1440)


class PartyResource(ColibriResource):
    term = fields.IntegerField(attribute='groupmember__group__term__decimal',
                               readonly=True, null=True)
    class Meta:
        queryset = Party.objects.all()
        allowed_methods = ['get']
        resource_name = "party"
        filtering = {
            "name": ('exact', 'startswith', 'iexact', 'istartswith',),
            "id": ('exact',),
            "term": ('exact',),
        }
        cache = SimpleCache(timeout=1440)
