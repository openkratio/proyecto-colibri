import datetime
from pytz import timezone

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as dj_timezone
from colibri.settings import TIME_ZONE


class Author(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        if self.user.first_name and self.user.last_name:
            return "%s %s" % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)

    models.signals.post_save.connect(create_user_profile, sender=User)

    def live_entry_set(self):
        return self.entry_set.filter(status=Entry.LIVE_STATUS)


class Category(models.Model):
    title = models.CharField(max_length=250,
        help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True,
        help_text='Suggested value automatically generated from title. '\
                  'Must be unique.')

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('blog_category_detail', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

    def live_entry_set(self):
        from blog.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)


class LiveEntryManager(models.Manager):

    def get_query_set(self):
        return super(LiveEntryManager,
            self).get_query_set().filter(status=self.model.LIVE_STATUS)


class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date='pub_date',
        help_text='Suggested value automatically generated from title. '\
                  'Must be unique.')
    body = models.TextField(help_text='Use Markdown to mark this up. '\
        'http://daringfireball.net/projects/markdown/syntax')
    pub_date = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=timezone(TIME_ZONE)))
    author = models.ForeignKey(Author)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        local_pub_date = dj_timezone.localtime(self.pub_date)
        return ('blog_entry_detail',
                (),
                {'year': local_pub_date.strftime("%Y"),
                 'month': local_pub_date.strftime("%b").lower(),
                 'day': local_pub_date.strftime("%d"),
                 'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

    objects = models.Manager()
    live = LiveEntryManager()
