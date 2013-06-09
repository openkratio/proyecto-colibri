# coding=utf-8
from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS

from vote.models import Voting, Vote, Session


class VoteManagerResource(ModelResource):
    class Meta:
        queryset = Vote.objects.filter()
        allowed_methods = ['get']


class VoteResource(VoteManagerResource):
    session_number = fields.IntegerField(
        attribute='voting__session__session', readonly=True)
    number = fields.IntegerField(attribute='voting__number', readonly=True)
    member = fields.ToOneField('member.api.MemberResource', 'member')

    class Meta(VoteManagerResource.Meta):
        resource_name = 'vote'
        filtering = {
            "session_number": ('exact',),
            "number": ('exact',),
        }

    def build_filters(self, filters=None):
        """
        if filters is None:
            raise InvalidFilterError("Filter fields  are necessaries.")
        if 'session' not in filters:
            raise InvalidFilterError("Session field is necessary.")
        if 'number' not in filters:
            raise InvalidFilterError("Number field is necessary.")
        """
        orm_filters = super(VoteResource, self).build_filters(filters)
        return orm_filters


class VoteFullResource(VoteManagerResource):
    member = fields.ToOneField('member.api.MemberResource', 'member')

    class Meta(VoteManagerResource.Meta):
        resource_name = 'vote_full'


class VotingManagerResource(ModelResource):
    class Meta:
        queryset = Voting.objects.all()
        allowed_methods = ['get']


class VotingResource(ModelResource):
    session = fields.ToOneField('vote.api.SessionResource', 'session')

    class Meta(VotingManagerResource.Meta):
        filtering = {
            "session": ALL_WITH_RELATIONS,
        }
        resource_name = 'voting'


class VotingFullResource(VotingManagerResource):
    votes = fields.ToManyField('vote.api.VoteResource', 'vote')

    class Meta(VotingManagerResource.Meta):
        filtering = {
            "session": ALL_WITH_RELATIONS,
        }
        resource_name = 'voting_full'


class SessionManagerResource(ModelResource):
    class Meta:
        queryset = Session.objects.all()
        allowed_methods = ['get', ]
        filtering = {
            "session": ('exact', 'in')
        }
        ordering = ['date']


class SessionResource(SessionManagerResource):
    class Meta(SessionManagerResource.Meta):
        resource_name = 'session'


class SessionFullResource(SessionManagerResource):
    class Meta(SessionManagerResource.Meta):
        resource_name = 'session_full'
