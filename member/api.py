from tastypie.resources import ModelResource
from tastypie import fields
from member.models import Member, MemberParty

class MemberResource(ModelResource):
    parties = fields.ToManyField('member.api.MemberPartyResource', 'memberparty_set')

    class Meta:
        queryset = Member.objects.all()
        allowed_methods = ['get']
        resource_name = "member"
    
    # with this method is not needed to add '?format=json'
    def determine_format(self, request): 
        return "application/json"         


class MemberPartyResource(ModelResource):
    member = fields.ToOneField('member.api.MemberResource', 'member')

    class Meta:
        queryset = MemberParty.objects.all()
        allowed_methods = ['get']
        fields = ['member']
        resource_name = "memberparty"
        include_resource_uri = False

    def determine_format(self, request): 
        return "application/json"         
