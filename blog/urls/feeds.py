from django.conf.urls import patterns, url

from blog.feeds import LatestEntries


urlpatterns = patterns('',
    url(r'^$', LatestEntries(), name='blog_feed'),)
