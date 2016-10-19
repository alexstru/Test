# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AboutMe'
        db.create_table(u'hello_aboutme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('jabber', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contacts', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'hello', ['AboutMe'])


    def backwards(self, orm):
        # Deleting model 'AboutMe'
        db.delete_table(u'hello_aboutme')


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
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['hello']