# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Seat.number'
        db.add_column('member_seat', 'number',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


        # Changing field 'Member.avatar'
        db.alter_column('member_member', 'avatar', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

    def backwards(self, orm):
        # Deleting field 'Seat.number'
        db.delete_column('member_seat', 'number')


        # Changing field 'Member.avatar'
        db.alter_column('member_member', 'avatar', self.gf('django.db.models.fields.files.ImageField')(default='Empty', max_length=100))

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
        'member.memberparty': {
            'Meta': {'object_name': 'MemberParty'},
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['member.Member']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parliamentarygroup.Party']"}),
            'seat': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['member.Seat']", 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'substitute': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'substitute'", 'null': 'True', 'to': "orm['member.Member']"})
        },
        'member.seat': {
            'Meta': {'object_name': 'Seat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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

    complete_apps = ['member']