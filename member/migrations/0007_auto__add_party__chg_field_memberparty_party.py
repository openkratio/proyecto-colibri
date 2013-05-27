# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Party'
        db.create_table('member_party', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('web', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('validate', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('member', ['Party'])


        # Changing field 'MemberParty.party'
        #db.alter_column('member_memberparty', 'party_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member.Party']))

    def backwards(self, orm):
        # Deleting model 'Party'
        db.delete_table('member_party')


        # Changing field 'MemberParty.party'
        db.alter_column('member_memberparty', 'party_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parliamentarygroup.Party']))

    models = {
        'member.member': {
            'Meta': {'object_name': 'Member'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'congress_web': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parties': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['member.Party']", 'through': "orm['member.MemberParty']", 'symmetrical': 'False'}),
            'second_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'member.memberparty': {
            'Meta': {'object_name': 'MemberParty'},
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['member.Member']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['member.Party']"}),
            'seat': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['member.Seat']", 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'})
        },
        'member.party': {
            'Meta': {'object_name': 'Party'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        'member.seat': {
            'Meta': {'object_name': 'Seat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['member']
