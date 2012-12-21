# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Shop.access_token'
        db.add_column('shopify_shop', 'access_token',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Shop.name'
        db.alter_column('shopify_shop', 'name', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Shop.access_token'
        db.delete_column('shopify_shop', 'access_token')


        # Changing field 'Shop.name'
        db.alter_column('shopify_shop', 'name', self.gf('django.db.models.fields.TextField')(default=0))

    models = {
        'shopify.shop': {
            'Meta': {'object_name': 'Shop'},
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'myshopify_domain': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['shopify']