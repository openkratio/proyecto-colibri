from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie import fields
from parliamentarygroup.api import PartyResource
from member.models import Member, MemberParty

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.all()
        allowed_methods = ['get']

class MemberPartyResource(ModelResource):
    party = fields.ForeignKey(PartyResource, 'party')
    member = fields.ForeignKey(MemberResource, 'member', full=True)
    class Meta:
        queryset = MemberParty.objects.all()
        allowed_methods = ['get']
        filtering = {
            "party": (ALL_WITH_RELATIONS),
        }
