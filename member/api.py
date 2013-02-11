from tastypie.resources import ModelResource
from tastypie import fields
from member.models import Member, MemberParty

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.all()
        allowed_methods = ['get']

class MemberPartyResource(ModelResource):
    member = fields.ToOneField('members.api.MemberResource', 'member')
    class Meta:
        queryset = MemberParty.objects.all()
        allowed_methods = ['get']
