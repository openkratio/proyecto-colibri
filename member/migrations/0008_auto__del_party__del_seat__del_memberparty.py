# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Party'
        db.delete_table('member_party')

        # Deleting model 'Seat'
        db.delete_table('member_seat')

        # Deleting model 'MemberParty'
        db.delete_table('member_memberparty')


    def backwards(self, orm):
        # Adding model 'Party'
        db.create_table('member_party', (
            ('web', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('validate', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('member', ['Party'])

        # Adding model 'Seat'
        db.create_table('member_seat', (
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('member', ['Seat'])

        # Adding model 'MemberParty'
        db.create_table('member_memberparty', (
            ('end_date', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('seat', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['member.Seat'], null=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member.Member'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member.Party'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('member', ['MemberParty'])


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
        }
    }

    complete_apps = ['member']