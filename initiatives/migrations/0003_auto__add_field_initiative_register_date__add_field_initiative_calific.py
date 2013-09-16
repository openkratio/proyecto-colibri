# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Initiative.register_date'
        db.add_column(u'initiatives_initiative', 'register_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Initiative.calification_date'
        db.add_column(u'initiatives_initiative', 'calification_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Initiative.register_date'
        db.delete_column(u'initiatives_initiative', 'register_date')

        # Deleting field 'Initiative.calification_date'
        db.delete_column(u'initiatives_initiative', 'calification_date')


    models = {
        u'initiatives.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'calification_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'register_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['term.Term']"})
        },
        u'initiatives.initiativetype': {
            'Meta': {'object_name': 'InitiativeType'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative_type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'initiatives.status': {
            'Meta': {'object_name': 'Status'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'follow': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['initiatives.Initiative']"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'term.term': {
            'Meta': {'object_name': 'Term'},
            'decimal': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 12, 0, 0)', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 12, 0, 0)'})
        }
    }

    complete_apps = ['initiatives']