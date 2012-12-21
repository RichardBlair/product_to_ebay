from django.db import models


class Shop(models.Model):
    myshopify_domain = models.TextField(unique=True)
    name = models.TextField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
