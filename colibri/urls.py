from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from commission.api import CommissionManagerResource
from initiatives.api import InitiativeResource
from member.api import MemberResource
from parliamentarygroup.api import GroupResource,\
                                   GroupManagerResource,\
                                   GroupMemberResource,\
                                   PartyResource
from vote.api import VotingResource, VoteResource, SessionResource,\
                     VotingFullResource, VoteFullResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(CommissionManagerResource())
v1_api.register(GroupManagerResource())
v1_api.register(GroupMemberResource())
v1_api.register(GroupResource())
v1_api.register(InitiativeResource())
v1_api.register(MemberResource())
v1_api.register(PartyResource())
v1_api.register(SessionResource())
v1_api.register(VoteFullResource())
v1_api.register(VoteResource())
v1_api.register(VotingFullResource())
v1_api.register(VotingResource())

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'documentacion/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^apps/$','main.views.apps', name="main_apps"),
    url(r'^somos/$','main.views.weare', name="main_weare"),
    url(r'^gracias/$','main.views.thanks', name="main_thanks"),
    url(r'^blog/author/', include('blog.urls.authors')),
    url(r'^blog/category/', include('blog.urls.categories')),
    url(r'^blog/feeds/', include('blog.urls.feeds')),
    url(r'^blog/', include('blog.urls.entries')),
    url(r'^$','main.views.index', name="main_index"),
)
