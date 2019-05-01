from django.conf.urls import url

from drawLocations.views import *

urlpatterns = [
    url(r'^$', DrawLocations.as_view()),

]
