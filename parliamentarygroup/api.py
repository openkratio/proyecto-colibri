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

class GroupPartyResource(ModelResource):
    party = fields.ToOneField('parliamentarygroup.api.PartyResource', 'party', full=True)
    class Meta:
        queryset = GroupParty.objects.all()
        allowed_methods = ['get']

class PartyResource(ModelResource):
    class Meta:
        queryset = Party.objects.all()
        allowed_methods = ['get']
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }

