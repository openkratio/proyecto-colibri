# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Term'
        db.create_table('term_term', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('roman', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('decimal', self.gf('django.db.models.fields.IntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 2, 0, 0))),
            ('end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 2, 0, 0), blank=True)),
        ))
        db.send_create_signal('term', ['Term'])


    def backwards(self, orm):
        # Deleting model 'Term'
        db.delete_table('term_term')


    models = {
        'term.term': {
            'Meta': {'object_name': 'Term'},
            'decimal': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 2, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 2, 0, 0)'})
        }
    }

    complete_apps = ['term']