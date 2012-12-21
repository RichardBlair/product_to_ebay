from django.db import models


class Shop(models.Model):
    myshopify_domain = models.TextField(unique=True)
    name = models.TextField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_username(self):
        return '%s' % (self.myshopify_domain)
