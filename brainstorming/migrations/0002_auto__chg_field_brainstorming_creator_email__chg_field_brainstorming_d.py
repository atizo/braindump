# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Brainstorming.creator_email'
        db.alter_column(u'brainstorming_brainstorming', 'creator_email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75))

        # Changing field 'Brainstorming.details'
        db.alter_column(u'brainstorming_brainstorming', 'details', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Idea.title'
        db.alter_column(u'brainstorming_idea', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

    def backwards(self, orm):

        # Changing field 'Brainstorming.creator_email'
        db.alter_column(u'brainstorming_brainstorming', 'creator_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))

        # Changing field 'Brainstorming.details'
        db.alter_column(u'brainstorming_brainstorming', 'details', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Idea.title'
        db.alter_column(u'brainstorming_idea', 'title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    models = {
        u'brainstorming.brainstorming': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Brainstorming'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['brainstorming']