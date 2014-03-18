# -*- coding: utf-8 -*-
from brainstorming.models import Brainstorming
from south.db import db
from south.v2 import SchemaMigration
from django.db.models import F
from django.db import transaction


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding field 'Brainstorming.idea_sequence'
        db.add_column(u'brainstorming_brainstorming', 'idea_sequence',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Idea.number'
        db.add_column(u'brainstorming_idea', 'number',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        for brainstorming in Brainstorming.objects.all():
            for idea in brainstorming.idea_set.all().order_by('created'):
                with transaction.atomic():
                    brainstorming.idea_sequence = F('idea_sequence') + 1
                    brainstorming.save()
                    idea.number = Brainstorming.objects.get(pk=brainstorming.pk).idea_sequence
                    idea.save()


    def backwards(self, orm):
        # Deleting field 'Brainstorming.idea_sequence'
        db.delete_column(u'brainstorming_brainstorming', 'idea_sequence')

        # Deleting field 'Idea.number'
        db.delete_column(u'brainstorming_idea', 'number')


    models = {
        u'brainstorming.brainstorming': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Brainstorming'},
            'created': (
            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'creator_ip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'idea_sequence': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': (
            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'brainstorming.brainstormingwatcher': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('brainstorming', 'email'),)",
                     'object_name': 'BrainstormingWatcher'},
            'brainstorming': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brainstorming.Brainstorming']"}),
            'created': (
            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': (
            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'brainstorming.emailverification': {
            'Meta': {'ordering': "['-created']", 'object_name': 'EmailVerification'},
            'created': (
            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified': (
            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'brainstorming.idea': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Idea'},
            'brainstorming': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brainstorming.Brainstorming']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': (
            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'creator_ip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'modified': (
            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ratings': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['brainstorming']