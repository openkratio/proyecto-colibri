# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Group.end_date'
        db.delete_column('parliamentarygroup_group', 'end_date')

        # Deleting field 'Group.start_date'
        db.delete_column('parliamentarygroup_group', 'start_date')

        # Deleting field 'GroupParty.end_date'
        db.delete_column('parliamentarygroup_groupparty', 'end_date')

        # Deleting field 'GroupParty.start_date'
        db.delete_column('parliamentarygroup_groupparty', 'start_date')


    def backwards(self, orm):
        # Adding field 'Group.end_date'
        db.add_column('parliamentarygroup_group', 'end_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Group.start_date'
        db.add_column('parliamentarygroup_group', 'start_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'GroupParty.end_date'
        db.add_column('parliamentarygroup_groupparty', 'end_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 24, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'GroupParty.start_date'
        db.add_column('parliamentarygroup_groupparty', 'start_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 24, 0, 0)),
                      keep_default=False)


    models = {
        'parliamentarygroup.color': {
            'Meta': {'object_name': 'Color'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'#000000'", 'max_length': '50'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Party']"})
        },
        'parliamentarygroup.group': {
            'Meta': {'object_name': 'Group'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'congress_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['term.Term']"}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'parliamentarygroup.groupparty': {
            'Meta': {'object_name': 'GroupParty'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Party']"})
        },
        'parliamentarygroup.party': {
            'Meta': {'object_name': 'Party'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        'term.term': {
            'Meta': {'object_name': 'Term'},
            'decimal': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 24, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 24, 0, 0)'})
        }
    }

    complete_apps = ['parliamentarygroup']