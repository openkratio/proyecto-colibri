# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Session'
        db.create_table('vote_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 23, 0, 0))),
        ))
        db.send_create_signal('vote', ['Session'])

        # Deleting field 'Voting.date'
        db.delete_column('vote_voting', 'date')


        # Renaming column for 'Voting.session' to match new field type.
        db.rename_column('vote_voting', 'session', 'session_id')
        # Changing field 'Voting.session'
        db.alter_column('vote_voting', 'session_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vote.Session']))
        # Adding index on 'Voting', fields ['session']
        db.create_index('vote_voting', ['session_id'])


    def backwards(self, orm):
        # Removing index on 'Voting', fields ['session']
        db.delete_index('vote_voting', ['session_id'])

        # Deleting model 'Session'
        db.delete_table('vote_session')

        # Adding field 'Voting.date'
        db.add_column('vote_voting', 'date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 12, 24, 0, 0)),
                      keep_default=False)


        # Renaming column for 'Voting.session' to match new field type.
        db.rename_column('vote_voting', 'session_id', 'session')
        # Changing field 'Voting.session'
        db.alter_column('vote_voting', 'session', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'member.member': {
            'Meta': {'object_name': 'Member'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'congress_web': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'second_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'vote.session': {
            'Meta': {'object_name': 'Session'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 23, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'vote.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['member.Member']"}),
            'vote': ('django.db.models.fields.CharField', [], {'default': "u'Empty'", 'max_length': '20'}),
            'voting': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['vote.Voting']"})
        },
        'vote.voting': {
            'Meta': {'object_name': 'Voting'},
            'abstains': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'against_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'assent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attendee': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'for_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'record_text': ('django.db.models.fields.TextField', [], {'default': "u'Empty'"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['vote.Session']"}),
            'subgroup_text': ('django.db.models.fields.TextField', [], {'default': "u'Empty'"}),
            'subgroup_title': ('django.db.models.fields.CharField', [], {'default': "u'Empty'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Empty'", 'max_length': '255'})
        }
    }

    complete_apps = ['vote']