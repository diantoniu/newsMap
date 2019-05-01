from django.http import HttpResponse
from django.views import View
from newsAnalyze.views import *
import folium
import pandas as pd
import numpy as np
from django.template import Context, loader
import os
from django.shortcuts import render_to_response

from django.views.generic import TemplateView


class DrawLocations(TemplateView):
    template_name = 'map/map.html'
    def draw(self, locations):
        data = pd.DataFrame({
            'name': locations[0],
            'lat': locations[1],
            'lon': locations[2],
            'value': locations[3]
        })

        #Make an empty map
        m = folium.Map(location=[10, 0], tiles="Mapbox Bright", zoom_start=2)

        # # I can add marker one by one on the map
        for i in range(0, len(data)):
            folium.Circle(
                location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                popup=data.iloc[i]['name'],
                radius=np.float32(data.iloc[i]['value']).item() * 10000,
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(m)

        #Save it as html
        m.save(os.path.join(os.path.dirname( __file__ ), '..', 'templates/map/map.html'))
    def get(self, *args, **kwargs):
        dateFrom = time.strptime(self.request.GET.get('dateFrom'), "%Y-%m-%d")
        dateTo = time.strptime(self.request.GET.get('dateTo'), "%Y-%m-%d")
        analyzer = NewsAnalyze()
        locations = analyzer.getLocationNameSize(dateFrom, dateTo)
        self.draw(locations)
        resp = super().get(*args, **kwargs)
        return resp
