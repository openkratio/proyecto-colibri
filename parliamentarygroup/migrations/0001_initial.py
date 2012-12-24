# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('parliamentarygroup_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('term', self.gf('django.db.models.fields.IntegerField')()),
            ('validate', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('parliamentarygroup', ['Group'])

        # Adding model 'Party'
        db.create_table('parliamentarygroup_party', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('web', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Group'])),
            ('validate', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('parliamentarygroup', ['Party'])

        # Adding model 'Color'
        db.create_table('parliamentarygroup_color', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='#000000', max_length=50)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Party'])),
        ))
        db.send_create_signal('parliamentarygroup', ['Color'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table('parliamentarygroup_group')

        # Deleting model 'Party'
        db.delete_table('parliamentarygroup_party')

        # Deleting model 'Color'
        db.delete_table('parliamentarygroup_color')


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
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'term': ('django.db.models.fields.IntegerField', [], {}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'parliamentarygroup.party': {
            'Meta': {'object_name': 'Party'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['parliamentarygroup']