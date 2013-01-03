# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EbaySettings'
        db.create_table('ebay_product_ebaysettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shopify.Shop'])),
        ))
        db.send_create_signal('ebay_product', ['EbaySettings'])


    def backwards(self, orm):
        # Deleting model 'EbaySettings'
        db.delete_table('ebay_product_ebaysettings')


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
        'ebay_product.ebaysettings': {
            'Meta': {'object_name': 'EbaySettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shopify.Shop']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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