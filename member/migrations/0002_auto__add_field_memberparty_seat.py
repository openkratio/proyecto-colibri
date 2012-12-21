# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MemberParty.seat'
        db.add_column('member_memberparty', 'seat',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member.Seat'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MemberParty.seat'
        db.delete_column('member_memberparty', 'seat_id')


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
        'member.memberparty': {
            'Meta': {'object_name': 'MemberParty'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['member.Member']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Party']"}),
            'seat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['member.Seat']", 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'substitute': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'substitute'", 'to': "orm['member.Member']"})
        },
        'member.seat': {
            'Meta': {'object_name': 'Seat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
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

    complete_apps = ['member']