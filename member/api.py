from tastypie.resources import ModelResource
from member.models import Member, MemberParty

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.all()
        allowed_methods = ['get']

class MemberPartyResource(ModelResource):
    class Meta:
        queryset = MemberParty.objects.all()
        allowed_methods = ['get']
