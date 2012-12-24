# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Group.term'
        db.alter_column('parliamentarygroup_group', 'term', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Group.end_date'
        db.alter_column('parliamentarygroup_group', 'end_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Group.start_date'
        db.alter_column('parliamentarygroup_group', 'start_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Party.web'
        db.alter_column('parliamentarygroup_party', 'web', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'Party.logo'
        db.alter_column('parliamentarygroup_party', 'logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

    def backwards(self, orm):

        # Changing field 'Group.term'
        db.alter_column('parliamentarygroup_group', 'term', self.gf('django.db.models.fields.IntegerField')(default=0))

        # Changing field 'Group.end_date'
        db.alter_column('parliamentarygroup_group', 'end_date', self.gf('django.db.models.fields.DateField')(default=None))

        # Changing field 'Group.start_date'
        db.alter_column('parliamentarygroup_group', 'start_date', self.gf('django.db.models.fields.DateField')(default=None))

        # Changing field 'Party.web'
        db.alter_column('parliamentarygroup_party', 'web', self.gf('django.db.models.fields.URLField')(default=None, max_length=200))

        # Changing field 'Party.logo'
        db.alter_column('parliamentarygroup_party', 'logo', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100))

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
            'term': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'parliamentarygroup.party': {
            'Meta': {'object_name': 'Party'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['parliamentarygroup']