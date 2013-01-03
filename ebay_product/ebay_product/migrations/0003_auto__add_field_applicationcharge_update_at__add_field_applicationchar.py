# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ApplicationCharge.update_at'
        db.add_column('ebay_product_applicationcharge', 'update_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 12, 29, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'ApplicationCharge.created_at'
        db.add_column('ebay_product_applicationcharge', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 12, 29, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ApplicationCharge.update_at'
        db.delete_column('ebay_product_applicationcharge', 'update_at')

        # Deleting field 'ApplicationCharge.created_at'
        db.delete_column('ebay_product_applicationcharge', 'created_at')


    models = {
        'ebay_product.applicationcharge': {
            'Meta': {'object_name': 'ApplicationCharge'},
            'charge_id': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shopify.Shop']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'update_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'shopify.shop': {
            'Meta': {'object_name': 'Shop'},
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'myshopify_domain': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ebay_product']