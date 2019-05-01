from django.http import HttpResponse
from django.views import View
from django.template import Context, loader
import os
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
import time
from drawLocations.views import *


class HomePage(TemplateView):
    template_name = 'home.html'

    def get(self, *args, **kwargs):
        try:
            dateFrom = time.strptime(self.request.GET.get('dateFrom'), "%Y-%m-%d")
            dateTo = time.strptime(self.request.GET.get('dateTo'), "%Y-%m-%d")
            if dateFrom <= dateTo:
                return DrawLocations.as_view()(self.request)
        except Exception:
            print(sys.exc_info())
        return super().get(*args, **kwargs)
