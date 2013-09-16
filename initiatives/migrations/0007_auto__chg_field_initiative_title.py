# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Initiative.title'
        db.alter_column(u'initiatives_initiative', 'title', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'Initiative.title'
        db.alter_column(u'initiatives_initiative', 'title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    models = {
        u'initiatives.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.Member']", 'symmetrical': 'False'}),
            'calification_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative_type': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'record': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'register_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['term.Term']"}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'member.member': {
            'Meta': {'object_name': 'Member'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'congress_id': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '32'}),
            'congress_web': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'second_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'term.term': {
            'Meta': {'object_name': 'Term'},
            'decimal': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 13, 0, 0)', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 13, 0, 0)'})
        }
    }

    complete_apps = ['initiatives']