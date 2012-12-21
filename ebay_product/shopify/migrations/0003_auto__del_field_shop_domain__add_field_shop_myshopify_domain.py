# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Shop.domain'
        db.delete_column('shopify_shop', 'domain')

        # Adding field 'Shop.myshopify_domain'
        db.add_column('shopify_shop', 'myshopify_domain',
                      self.gf('django.db.models.fields.TextField')(default=0, unique=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Shop.domain'
        db.add_column('shopify_shop', 'domain',
                      self.gf('django.db.models.fields.TextField')(default=0),
                      keep_default=False)

        # Deleting field 'Shop.myshopify_domain'
        db.delete_column('shopify_shop', 'myshopify_domain')


    models = {
        'shopify.shop': {
            'Meta': {'object_name': 'Shop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'myshopify_domain': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['shopify']