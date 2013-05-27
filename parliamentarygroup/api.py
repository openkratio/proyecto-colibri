from tastypie.resources import ModelResource
from tastypie import fields
from parliamentarygroup.models import Group, Party, GroupParty

class GroupResource(ModelResource):
    parties = fields.ToManyField('parliamentarygroup.api.GroupPartyResource', 'groupparty_set', related_name='party', full=True)
    class Meta:
        queryset = Group.objects.all()
        allowed_methods = ['get']
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }
        resource_name = "group"

class GroupPartyResource(ModelResource):
    party = fields.ToOneField('parliamentarygroup.api.PartyResource', 'party', full=True)

    class Meta:
        queryset = GroupParty.objects.all()
        allowed_methods = ['get']
        resource_name = "partyresource"


class PartyResource(ModelResource):
    members = fields.ToManyField('member.api.MemberPartyResource',
                                 attribute=lambda bundle: bundle.obj.memberparty_set.filter(party=bundle.obj) or bundle.obj.memberparty_set, full=True)

    class Meta:
        queryset = Party.objects.all()
        allowed_methods = ['get']
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }
        resource_name = "party"
