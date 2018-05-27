from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^/$', views.index),
    url(r'/events', views.events),
    url(r'/delevent', views.delete_event),
    url(r'/turn_points_on', views.turn_points_on),
    url(r'/turn_points_off', views.turn_points_off),
    url(r'^/set_maxPoints', views.set_max_points)
]