from tastypie.resources import ModelResource
from parliamentarygroup.models import Group, Party

class GroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        allowed_methods = ['get']
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }

class PartyResource(ModelResource):
    class Meta:
        queryset = Party.objects.all()
        allowed_methods = ['get']
        filtering = {
            "name": ('exact',),
            "id": ('exact',),
        }
