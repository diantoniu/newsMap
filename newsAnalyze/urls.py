from django.conf.urls import url

from newsAnalyze.views import *

urlpatterns = [
    url(r'^$', NewsAnalyze.as_view()),

]
