# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Voting.subgroup_title'
        db.alter_column(u'vote_voting', 'subgroup_title', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'Voting.subgroup_title'
        db.alter_column(u'vote_voting', 'subgroup_title', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        u'member.member': {
            'Meta': {'object_name': 'Member'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'congress_id': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '32'}),
            'congress_web': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'second_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'vote.session': {
            'Meta': {'object_name': 'Session'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 6, 9, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'vote.vote': {
            'Meta': {'object_name': 'Vote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['member.Member']"}),
            'vote': ('django.db.models.fields.CharField', [], {'default': "u'Empty'", 'max_length': '20'}),
            'voting': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['vote.Voting']"})
        },
        u'vote.voting': {
            'Meta': {'object_name': 'Voting'},
            'abstains': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'against_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'assent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attendee': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'for_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'record_text': ('django.db.models.fields.TextField', [], {'default': "u'Empty'"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['vote.Session']"}),
            'subgroup_text': ('django.db.models.fields.TextField', [], {'default': "u'Empty'"}),
            'subgroup_title': ('django.db.models.fields.TextField', [], {'default': "u'Empty'"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Empty'", 'max_length': '255'})
        }
    }

    complete_apps = ['vote']