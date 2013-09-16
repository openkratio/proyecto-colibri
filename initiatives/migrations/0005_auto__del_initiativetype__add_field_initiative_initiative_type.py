# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'InitiativeType'
        db.delete_table(u'initiatives_initiativetype')

        # Adding field 'Initiative.initiative_type'
        db.add_column(u'initiatives_initiative', 'initiative_type',
                      self.gf('django.db.models.fields.CharField')(max_length=150, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'InitiativeType'
        db.create_table(u'initiatives_initiativetype', (
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('initiative_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'initiatives', ['InitiativeType'])

        # Deleting field 'Initiative.initiative_type'
        db.delete_column(u'initiatives_initiative', 'initiative_type')


    models = {
        u'initiatives.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'calification_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative_type': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'record': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'register_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['term.Term']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
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