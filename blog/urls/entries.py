from django.conf.urls import patterns, url
from django.views.generic.dates import (ArchiveIndexView, DateDetailView,
    DayArchiveView, MonthArchiveView, YearArchiveView)

from blog.models import Entry


urlpatterns = patterns('',
    url(r'^$',
        ArchiveIndexView.as_view(
            allow_future=True,
            date_field='pub_date',
            queryset=Entry.live.all()
        ),
        name='blog_entry_archive'
    ),

    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            date_field='pub_date',
            make_object_list=True,
            queryset=Entry.live.all()
        ),
        name='blog_entry_archive_year'
    ),

    url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/$',
        MonthArchiveView.as_view(
            date_field='pub_date',
            queryset=Entry.live.all()
        ),
        name='blog_entry_archive_month'
    ),

    url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/(?P<day>\d{2})/$',
        DayArchiveView.as_view(
            date_field='pub_date',
            queryset=Entry.live.all()
        ),
        name='blog_entry_archive_day'
    ),

    url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(
            date_field='pub_date',
            queryset=Entry.objects.exclude(status=Entry.HIDDEN_STATUS),
        ),
        name='blog_entry_detail'
    ),
)
