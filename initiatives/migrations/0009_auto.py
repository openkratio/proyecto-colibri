# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field comissions on 'Initiative'
        m2m_table_name = db.shorten_name(u'initiatives_initiative_comissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('initiative', models.ForeignKey(orm[u'initiatives.initiative'], null=False)),
            ('commission', models.ForeignKey(orm[u'commission.commission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['initiative_id', 'commission_id'])


    def backwards(self, orm):
        # Removing M2M table for field comissions on 'Initiative'
        db.delete_table(db.shorten_name(u'initiatives_initiative_comissions'))


    models = {
        u'commission.commission': {
            'Meta': {'object_name': 'Commission'},
            'congress_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'congress_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['term.Term']"})
        },
        u'initiatives.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.Member']", 'symmetrical': 'False'}),
            'author_group': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['parliamentarygroup.Group']", 'symmetrical': 'False'}),
            'calification_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'comissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['commission.Commission']", 'symmetrical': 'False'}),
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
        u'parliamentarygroup.group': {
            'Meta': {'object_name': 'Group'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'congress_id': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '32'}),
            'congress_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.Member']", 'through': u"orm['parliamentarygroup.GroupMember']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['term.Term']"}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'parliamentarygroup.groupmember': {
            'Meta': {'object_name': 'GroupMember'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parliamentarygroup.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Member']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parliamentarygroup.Party']", 'null': 'True'})
        },
        u'parliamentarygroup.party': {
            'Meta': {'object_name': 'Party'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'term.term': {
            'Meta': {'object_name': 'Term'},
            'decimal': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 18, 0, 0)', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 18, 0, 0)'})
        }
    }

    complete_apps = ['initiatives']