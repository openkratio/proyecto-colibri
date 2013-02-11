from tastypie.resources import ModelResource
from tastypie import fields
from member.models import Member, MemberParty

class MemberResource(ModelResource):
    parties = fields.ToManyField('parliamentarygroup.api.PartyResource', 'memberparty_set', related_name='party')
    class Meta:
        queryset = Member.objects.all()
        allowed_methods = ['get']

class MemberPartyResource(ModelResource):
    member = fields.ToOneField('members.api.MemberResource', 'member')
    party = fields.ToOneField('members.api.PartyResource', 'party')
    class Meta:
        queryset = MemberParty.objects.all()
        allowed_methods = ['get']
