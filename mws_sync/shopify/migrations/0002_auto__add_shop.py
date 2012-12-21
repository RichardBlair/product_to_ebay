# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shop'
        db.create_table('shopify_shop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('domain', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('shopify', ['Shop'])


    def backwards(self, orm):
        # Deleting model 'Shop'
        db.delete_table('shopify_shop')


    models = {
        'shopify.shop': {
            'Meta': {'object_name': 'Shop'},
            'domain': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['shopify']