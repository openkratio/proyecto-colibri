# coding=utf-8
from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.exceptions import InvalidFilterError
from tastypie.resources import ALL_WITH_RELATIONS, ALL

from main.api import ColibriResource
from vote.models import Voting, Vote, Session


class VoteManagerResource(ColibriResource):
    class Meta:
        queryset = Vote.objects.all().select_related(
            'voting__session', 'member')
        allowed_methods = ['get']
        cache = SimpleCache(cache_name='default', timeout=1440)


class VoteResource(VoteManagerResource):
    session_number = fields.IntegerField(
        attribute='voting__session__session', readonly=True)
    number = fields.IntegerField(attribute='voting__number', readonly=True)
    member = fields.ToOneField('member.api.MemberResource', 'member')
    date = fields.DateField(
        attribute='voting__session__date', readonly=True)

    class Meta(VoteManagerResource.Meta):
        resource_name = 'vote'
        filtering = {
            "session_number": ('exact',),
            "number": ('exact',),
            "member": ('exact', ),
            "date": ALL
        }

    def build_filters(self, filters=None):
        if filters is None:
            raise InvalidFilterError("Filter fields  are necessaries.")
        if 'session' not in filters and 'member' not in filters:
            raise InvalidFilterError("Session or Member field is necessary.")

        if 'number' not in filters:
            raise InvalidFilterError("Number field is necessary.")

        orm_filters = super(VoteResource, self).build_filters(filters)
        return orm_filters


class VoteFullResource(VoteManagerResource):
    member = fields.ToOneField('member.api.MemberResource', 'member')

    class Meta(VoteManagerResource.Meta):
        resource_name = 'vote_full'
        filtering = {
            "member": ALL_WITH_RELATIONS,
            "vote": ('exact',),
        }



class VotingManagerResource(ColibriResource):
    class Meta:
        queryset = Voting.objects.all()
        allowed_methods = ['get']
        cache = SimpleCache(cache_name='default', timeout=1440)

class VotingResource(VotingManagerResource):
    session = fields.ForeignKey('vote.api.SessionResource', 'session')

    class Meta(VotingManagerResource.Meta):
        exclude = ['session']
        filtering = {
            "session": ALL_WITH_RELATIONS,
        }
        queryset = Voting.objects.all().select_related('session')
        resource_name = 'voting'


class VotingFullResource(VotingManagerResource):
    votes = fields.ToManyField('vote.api.VoteFullResource', 'vote_set', full=True)
    session = fields.ForeignKey('vote.api.SessionResource', 'session')

    class Meta(VotingManagerResource.Meta):
        queryset = Voting.objects.prefetch_related('session', 'vote_set', 'vote_set__member')
        exclude = ['session']
        filtering = {
            "session": ALL_WITH_RELATIONS,
        }
        resource_name = 'voting_full'


class SessionManagerResource(ColibriResource):
    class Meta:
        queryset = Session.objects.all()
        allowed_methods = ['get', ]
        filtering = {
            "session": ('exact', 'in'),
            "date": ALL,
        }
        ordering = ['date']
        cache = SimpleCache(cache_name='default', timeout=1440)


class SessionResource(SessionManagerResource):
    votings = fields.ToManyField('vote.api.VotingFullResource', 'voting_set')

    class Meta(SessionManagerResource.Meta):
        resource_name = 'session'
