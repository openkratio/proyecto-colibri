# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Initiative.tramitation_type'
        db.delete_column(u'initiatives_initiative', 'tramitation_type')

        # Deleting field 'Initiative.initiative_type'
        db.delete_column(u'initiatives_initiative', 'initiative_type')

        # Deleting field 'Initiative.title'
        db.delete_column(u'initiatives_initiative', 'title')

        # Deleting field 'Initiative.register_date'
        db.delete_column(u'initiatives_initiative', 'register_date')

        # Deleting field 'Initiative.author_text'
        db.delete_column(u'initiatives_initiative', 'author_text')

        # Deleting field 'Initiative.calification_date'
        db.delete_column(u'initiatives_initiative', 'calification_date')

        # Removing M2M table for field author on 'Initiative'
        db.delete_table(db.shorten_name(u'initiatives_initiative_author'))


    def backwards(self, orm):
        # Adding field 'Initiative.tramitation_type'
        db.add_column(u'initiatives_initiative', 'tramitation_type',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Adding field 'Initiative.initiative_type'
        db.add_column(u'initiatives_initiative', 'initiative_type',
                      self.gf('django.db.models.fields.IntegerField')(default=None),
                      keep_default=False)

        # Adding field 'Initiative.title'
        db.add_column(u'initiatives_initiative', 'title',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255),
                      keep_default=False)

        # Adding field 'Initiative.register_date'
        db.add_column(u'initiatives_initiative', 'register_date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'Initiative.author_text'
        db.add_column(u'initiatives_initiative', 'author_text',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Adding field 'Initiative.calification_date'
        db.add_column(u'initiatives_initiative', 'calification_date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding M2M table for field author on 'Initiative'
        m2m_table_name = db.shorten_name(u'initiatives_initiative_author')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('initiative', models.ForeignKey(orm[u'initiatives.initiative'], null=False)),
            ('member', models.ForeignKey(orm[u'member.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['initiative_id', 'member_id'])


    models = {
        u'initiatives.initiative': {
            'Meta': {'object_name': 'Initiative'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
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