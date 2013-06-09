from django.conf.urls import patterns, include, url
from tastypie.api import Api
from parliamentarygroup.api import GroupResource,\
                                   GroupMemberResource,\
                                   PartyResource
from member.api import MemberResource
from vote.api import VotingResource, VoteResource, SessionResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(GroupMemberResource())
v1_api.register(GroupResource())
v1_api.register(MemberResource())
v1_api.register(PartyResource())
v1_api.register(SessionResource())
v1_api.register(VotingResource())
v1_api.register(VoteResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^documentacion/$','main.views.documentation', name="main_documentation"),
    url(r'^somos/$','main.views.weare', name="main_weare"),
    url(r'^$','main.views.index', name="main_index"),
)
