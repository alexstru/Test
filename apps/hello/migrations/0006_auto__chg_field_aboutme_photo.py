# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AboutMe.photo'
        db.alter_column(u'hello_aboutme', 'photo', self.gf('smartfields.fields.ImageField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'AboutMe.photo'
        db.alter_column(u'hello_aboutme', 'photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

    models = {
        u'hello.aboutme': {
            'Meta': {'object_name': 'AboutMe'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'contacts': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'photo': ('smartfields.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'hello.modelschange': {
            'Meta': {'object_name': 'ModelsChange'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'hello.requestcontent': {
            'Meta': {'object_name': 'RequestContent'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'path': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'status_code': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['hello']