# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("term", "0001_initial"),
    )

    def forwards(self, orm):
        # Renaming column for 'Group.term' to match new field type.
        db.rename_column('parliamentarygroup_group', 'term', 'term_id')
        # Changing field 'Group.term'
        db.alter_column('parliamentarygroup_group', 'term_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['term.Term']))
        # Adding index on 'Group', fields ['term']
        db.create_index('parliamentarygroup_group', ['term_id'])


    def backwards(self, orm):
        # Removing index on 'Group', fields ['term']
        db.delete_index('parliamentarygroup_group', ['term_id'])


        # Renaming column for 'Group.term' to match new field type.
        db.rename_column('parliamentarygroup_group', 'term_id', 'term')
        # Changing field 'Group.term'
        db.alter_column('parliamentarygroup_group', 'term', self.gf('django.db.models.fields.IntegerField')(null=True))

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
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['term.Term']"}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'parliamentarygroup.groupparty': {
            'Meta': {'object_name': 'GroupParty'},
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 2, 0, 0)', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Party']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 2, 0, 0)'})
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
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 2, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 2, 0, 0)'})
        }
    }

    complete_apps = ['parliamentarygroup']
