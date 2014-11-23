from django.conf.urls import patterns, url

from .views import (StationListView, MeterListView, MeterDetailView,
        LogListView, MeterInfoListView, ModeListView)


urlpatterns = patterns('',
        url(r'^stations/$',
            StationListView.as_view(), name='list_stations'),
        url(r'^stations/(?P<pk>\d+)/meters/$',
            MeterListView.as_view(), name='station_meters_list'),
        url(r'^meter/(?P<pk>\d+)/$',
            MeterDetailView.as_view(), name='meter_detail'),
        url(r'^logs/$',
            LogListView.as_view(), name='list_logs'),
        url(r'^meter_infos/$',
            MeterInfoListView.as_view(), name='list_meter_infos'),
        url(r'^modes/$',
            ModeListView.as_view(), name='list_modes'),
        url(r'^accounts/login/$',
            'django.contrib.auth.views.login', name='login'),
        url(r'^accounts/logout/$',
            'django.contrib.auth.views.logout_then_login', name='logout'),
)
