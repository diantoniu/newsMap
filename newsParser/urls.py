from django.conf.urls import url

from newsParser.views import *

urlpatterns = [
    url(r'^$', NewsView.as_view()),

]
