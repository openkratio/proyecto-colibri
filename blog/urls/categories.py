from django.conf.urls import patterns, url
from django.views.generic.list import ListView

from blog.models import Category


urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Category.objects.all()),
        name='blog_category_list'),
    url(r'^(?P<slug>[-\w]+)/$',
        'blog.views.category_detail',
        name='blog_category_detail'),
)
