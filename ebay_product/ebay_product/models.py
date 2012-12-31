from django.db import models

from shopify.models import Shop


class EbaySettings(models.Model):
    token = models.CharField(max_length=200)
    shop = models.ForeignKey(Shop)


class ApplicationCharge(models.Model):
    CHARGE_STATUS = (
        (1, 'Active'),
        (2, 'Suspended'),
        (3, 'Inactive'),
        (4, 'Pending')
    )

    shop = models.ForeignKey(Shop)
    status = models.IntegerField(choices=CHARGE_STATUS, default=4)
    price = models.FloatField()
    name = models.CharField(max_length=150)
    charge_id = models.IntegerField()
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
