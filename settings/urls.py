from django.contrib import admin
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^/$', views.index),
    url(r'events', views.events),
    url(r'delevent', views.delete_event),
    url(r'turn_points_on', views.turn_points_on),
    url(r'turn_points_off', views.turn_points_off),
    url(r'^set_maxPoints', views.set_max_points),
    url(r'levels', views.levels),
    url(r'^set_maxLevel', views.set_max_level),
    url(r'^add_level_option', views.add_level_option),
    url(r'^deloption', views.delete_option),
    url(r'^set_level_amount', views.set_level_amount),
    url(r'^turnoff_level', views.turnoff_level),
    url(r'^turnon_level', views.turnon_level),
]
