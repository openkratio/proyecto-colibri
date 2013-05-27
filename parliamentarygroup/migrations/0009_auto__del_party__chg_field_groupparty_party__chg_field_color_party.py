# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Party'
        db.delete_table('parliamentarygroup_party')


        # Changing field 'GroupParty.party'
        #db.alter_column('parliamentarygroup_groupparty', 'party_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member.Party']))

        # Changing field 'Color.party'
        db.alter_column('parliamentarygroup_color', 'party_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member.Party']))

    def backwards(self, orm):
        # Adding model 'Party'
        db.create_table('parliamentarygroup_party', (
            ('web', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('validate', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('parliamentarygroup', ['Party'])


        # Changing field 'GroupParty.party'
        db.alter_column('parliamentarygroup_groupparty', 'party_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Party']))

        # Changing field 'Color.party'
        db.alter_column('parliamentarygroup_color', 'party_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Party']))

    models = {
        'member.party': {
            'Meta': {'object_name': 'Party'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        'parliamentarygroup.color': {
            'Meta': {'object_name': 'Color'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'#000000'", 'max_length': '50'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['member.Party']"})
        },
        'parliamentarygroup.group': {
            'Meta': {'object_name': 'Group'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'congress_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parties': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['member.Party']", 'through': "orm['parliamentarygroup.GroupParty']", 'symmetrical': 'False'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['term.Term']"}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'parliamentarygroup.groupparty': {
            'Meta': {'object_name': 'GroupParty'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['member.Party']"})
        },
        'term.term': {
            'Meta': {'object_name': 'Term'},
            'decimal': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 22, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 22, 0, 0)'})
        }
    }

    complete_apps = ['parliamentarygroup']
