from django.conf.urls import url

from homePage.views import *

urlpatterns = [
    url(r'^$', HomePage.as_view()),

]
