# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("member", "0001_initial"),
    )

    def forwards(self, orm):
        # Deleting model 'GroupParty'
        db.delete_table('parliamentarygroup_groupparty')

        # Deleting model 'Color'
        db.delete_table('parliamentarygroup_color')

        # Adding model 'Party'
        db.create_table('parliamentarygroup_party', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('web', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('validate', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('parliamentarygroup', ['Party'])

        # Adding model 'GroupMember'
        db.create_table('parliamentarygroup_groupmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Group'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member.Member'])),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Party'], null=True)),
        ))
        db.send_create_signal('parliamentarygroup', ['GroupMember'])


    def backwards(self, orm):
        # Adding model 'GroupParty'
        db.create_table('parliamentarygroup_groupparty', (
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member.Party'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Group'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('parliamentarygroup', ['GroupParty'])

        # Adding model 'Color'
        db.create_table('parliamentarygroup_color', (
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member.Party'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='#000000', max_length=50)),
        ))
        db.send_create_signal('parliamentarygroup', ['Color'])

        # Deleting model 'Party'
        db.delete_table('parliamentarygroup_party')

        # Deleting model 'GroupMember'
        db.delete_table('parliamentarygroup_groupmember')


    models = {
        'member.member': {
            'Meta': {'object_name': 'Member'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
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
        'parliamentarygroup.group': {
            'Meta': {'object_name': 'Group'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'congress_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['term.Term']"}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'parliamentarygroup.groupmember': {
            'Meta': {'object_name': 'GroupMember'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['member.Member']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Party']", 'null': 'True'})
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
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 27, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 27, 0, 0)'})
        }
    }

    complete_apps = ['parliamentarygroup']
