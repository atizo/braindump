# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brainstorming'
        db.create_table(u'brainstorming_brainstorming', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('id', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('creator_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'brainstorming', ['Brainstorming'])

        # Adding model 'Idea'
        db.create_table(u'brainstorming_idea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('brainstorming', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brainstorming.Brainstorming'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'brainstorming', ['Idea'])

        # Adding model 'BrainstormingWatcher'
        db.create_table(u'brainstorming_brainstormingwatcher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('brainstorming', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brainstorming.Brainstorming'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'brainstorming', ['BrainstormingWatcher'])

        # Adding unique constraint on 'BrainstormingWatcher', fields ['brainstorming', 'email']
        db.create_unique(u'brainstorming_brainstormingwatcher', ['brainstorming_id', 'email'])


    def backwards(self, orm):
        # Removing unique constraint on 'BrainstormingWatcher', fields ['brainstorming', 'email']
        db.delete_unique(u'brainstorming_brainstormingwatcher', ['brainstorming_id', 'email'])

        # Deleting model 'Brainstorming'
        db.delete_table(u'brainstorming_brainstorming')

        # Deleting model 'Idea'
        db.delete_table(u'brainstorming_idea')

        # Deleting model 'BrainstormingWatcher'
        db.delete_table(u'brainstorming_brainstormingwatcher')


    models = {
        u'brainstorming.brainstorming': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Brainstorming'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['brainstorming']