# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InitiativeType'
        db.create_table(u'initiatives_initiativetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('initiative_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'initiatives', ['InitiativeType'])

        # Adding model 'Initiative'
        db.create_table(u'initiatives_initiative', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['term.Term'])),
            ('initiative_type', self.gf('django.db.models.fields.IntegerField')()),
            ('record', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('register_date', self.gf('django.db.models.fields.DateField')()),
            ('calification_date', self.gf('django.db.models.fields.DateField')()),
            ('author_text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tramitation_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'initiatives', ['Initiative'])

        # Adding M2M table for field author on 'Initiative'
        m2m_table_name = db.shorten_name(u'initiatives_initiative_author')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('initiative', models.ForeignKey(orm[u'initiatives.initiative'], null=False)),
            ('member', models.ForeignKey(orm[u'member.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['initiative_id', 'member_id'])

        # Adding model 'Status'
        db.create_table(u'initiatives_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('follow', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('initiative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['initiatives.Initiative'])),
        ))
        db.send_create_signal(u'initiatives', ['Status'])


    def backwards(self, orm):
        # Deleting model 'InitiativeType'
        db.delete_table(u'initiatives_initiativetype')

        # Deleting model 'Initiative'
        db.delete_table(u'initiatives_initiative')

        # Removing M2M table for field author on 'Initiative'
        db.delete_table(db.shorten_name(u'initiatives_initiative_author'))

        # Deleting model 'Status'
        db.delete_table(u'initiatives_status')


    models = {
        u'initiatives.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.Member']", 'symmetrical': 'False'}),
            'author_text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'calification_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative_type': ('django.db.models.fields.IntegerField', [], {}),
            'record': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'register_date': ('django.db.models.fields.DateField', [], {}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['term.Term']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tramitation_type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 12, 0, 0)', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 12, 0, 0)'})
        }
    }

    complete_apps = ['initiatives']