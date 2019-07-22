from django.conf.urls import url
from . import views


urlpatterns=[
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    
    url(r'^trips/new$', views.new_trip),
    url(r'^trips/new/add$', views.add_new_trip),
    url(r'^trips/(?P<trip_id>\d+)$', views.display_trip),
    url(r'^trips/(?P<trip_id>\d+)/edit$', views.edit_trip),
    url(r'^trips/(?P<trip_id>\d+)/edit/process$', views.process_edit),
    url(r'^trips/(?P<trip_id>\d+)/delete$', views.remove_trip)
]
