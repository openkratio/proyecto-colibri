from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.bundle import Bundle
from vote.models import  Voting, Vote
from tastypie.exceptions import InvalidFilterError

class VotingResource(ModelResource):
    class Meta:
        queryset = Voting.objects.all()
        allowed_methods = ['get']
        filtering = {
                    "session": ('exact',),
                    "number": ('exact',),
        }

class VoteResource(ModelResource):
    session = fields.IntegerField(attribute='voting__session', readonly=True)
    number = fields.IntegerField(attribute='voting__number', readonly=True)
    
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

    def apply_filters(self, request, applicable_filters):
        semi_filtered = super(VoteResource, self).apply_filters(request, applicable_filters)

        return semi_filtered
