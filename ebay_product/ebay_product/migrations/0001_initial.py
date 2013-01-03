# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ApplicationCharge'
        db.create_table('ebay_product_applicationcharge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shopify.Shop'])),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('ebay_product', ['ApplicationCharge'])


    def backwards(self, orm):
        # Deleting model 'ApplicationCharge'
        db.delete_table('ebay_product_applicationcharge')


    models = {
        'ebay_product.applicationcharge': {
            'Meta': {'object_name': 'ApplicationCharge'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shopify.Shop']"}),
            'status': ('django.db.models.fields.IntegerField', [], {})
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