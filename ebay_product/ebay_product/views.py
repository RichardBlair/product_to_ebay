from django.http import HttpResponse
from django.views.generic import View, TemplateView


class InstallView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("")
