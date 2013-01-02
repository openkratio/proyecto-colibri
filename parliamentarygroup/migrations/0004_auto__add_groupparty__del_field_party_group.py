# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupParty'
        db.create_table('parliamentarygroup_groupparty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Group'])),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Party'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 2, 0, 0))),
            ('end_date', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('parliamentarygroup', ['GroupParty'])

        # Deleting field 'Party.group'
        db.delete_column('parliamentarygroup_party', 'group_id')


    def backwards(self, orm):
        # Deleting model 'GroupParty'
        db.delete_table('parliamentarygroup_groupparty')

        # Adding field 'Party.group'
        db.add_column('parliamentarygroup_party', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Group'], null=True),
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
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'term': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'parliamentarygroup.groupparty': {
            'Meta': {'object_name': 'GroupParty'},
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
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
        }
    }

    complete_apps = ['parliamentarygroup']