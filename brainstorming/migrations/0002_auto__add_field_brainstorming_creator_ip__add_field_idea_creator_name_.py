# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Brainstorming.creator_ip'
        db.add_column(u'brainstorming_brainstorming', 'creator_ip',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Idea.creator_name'
        db.add_column(u'brainstorming_idea', 'creator_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Idea.creator_ip'
        db.add_column(u'brainstorming_idea', 'creator_ip',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Brainstorming.creator_ip'
        db.delete_column(u'brainstorming_brainstorming', 'creator_ip')

        # Deleting field 'Idea.creator_name'
        db.delete_column(u'brainstorming_idea', 'creator_name')

        # Deleting field 'Idea.creator_ip'
        db.delete_column(u'brainstorming_idea', 'creator_ip')


    models = {
        u'brainstorming.brainstorming': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Brainstorming'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'creator_ip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'brainstorming.brainstormingwatcher': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('brainstorming', 'email'),)", 'object_name': 'BrainstormingWatcher'},
            'brainstorming': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brainstorming.Brainstorming']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'brainstorming.idea': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Idea'},
            'brainstorming': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brainstorming.Brainstorming']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator_ip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['brainstorming']