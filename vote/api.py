# coding=utf-8

from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie import fields

from tastypie.exceptions import InvalidFilterError

from vote.models import Voting, Vote, Session


class VoteResource(ModelResource):
    session = fields.IntegerField(
        attribute='voting__session__session', readonly=True)
    number = fields.IntegerField(attribute='voting__number', readonly=True)
    member = fields.ToOneField('member.api.MemberResource', 'member')

    class Meta:
        resource_name = 'vote'
        queryset = Vote.objects.filter()
        allowed_methods = ['get']
        filtering = {
            "session": ('exact',),
            "number": ('exact',),
        }

    def build_filters(self, filters=None):
        if filters is None:
            raise InvalidFilterError("Filter fields  are necessaries.")

        if 'session' not in filters:
            raise InvalidFilterError("Session field is necessary.")

        if 'number' not in filters:
            raise InvalidFilterError("Number field is necessary.")

        orm_filters = super(VoteResource, self).build_filters(filters)
        return orm_filters


class VotingResource(ModelResource):
    session = fields.ToOneField('vote.api.SessionResource', 'session')

    class Meta:
        resource_name = 'voting'
        queryset = Voting.objects.all()
        allowed_methods = ['get']
        filtering = {
            "session": ALL_WITH_RELATIONS,
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        # map session filter to session number instead of id
        if 'session' in filters and filters['session']:
            filters.setdefault(
                'session__session__in', filters['session'])
            del filters['session']
        orm_filters = super(VotingResource, self).build_filters(filters)
        return orm_filters


class SessionResource(ModelResource):
    class Meta:
        resource_name = 'session'
        queryset = Session.objects.all()
        allowed_methods = ['get', ]
        filtering = {
            "session": ('exact', 'in')
        }
