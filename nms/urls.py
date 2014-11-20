from django.conf.urls import patterns, url

from .views import StationListView, MeterListView, MeterDetailView


urlpatterns = patterns('',
        url(r'^$',
            StationListView.as_view(), name='list_stations'),
        url(r'^stations/(?P<pk>\d+)/meters/$',
            MeterListView.as_view(), name='station_meters_list'),
        url(r'^meter/(?P<pk>\d+)/$',
            MeterDetailView.as_view(), name='meter_detail'),
        url(r'^accounts/login/$',
            'django.contrib.auth.views.login', name='login'),
        url(r'^accounts/logout/$',
            'django.contrib.auth.views.logout_then_login', name='logout'),
)
