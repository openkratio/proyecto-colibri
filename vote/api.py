from tastypie.resources import ModelResource
from tastypie import fields
from vote.models import  Voting, Vote

class VotingResource(ModelResource):
    class Meta:
        queryset = Voting.objects.all()
        allowed_methods = ['get']

class VoteResource(ModelResource):
    session = fields.IntegerField(attribute='voting__session', readonly=True)
    number = fields.IntegerField(attribute='voting__number', readonly=True)
    class Meta:
        queryset = Vote.objects.all()
        allowed_methods = ['get']
        filtering = {
                    "session": ('exact',),
                    "number": ('exact',),
            }
