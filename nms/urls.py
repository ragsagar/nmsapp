from django.conf.urls import patterns, url

from .views import (StationListView, MeterListView, MeterDetailView,
        LogListView, MeterInfoListView, ModeListView, CreateModeView,
        CreateMeterInfoView, CreateStationView)


urlpatterns = patterns('',
        url(r'^stations/$',
            StationListView.as_view(), name='list_stations'),
        url(r'^stations/(?P<pk>\d+)/meters/$',
            MeterListView.as_view(), name='station_meters_list'),
        url(r'^stations/create/$',
            CreateStationView.as_view(), name='create_station'),
        url(r'^meter/(?P<pk>\d+)/$',
            MeterDetailView.as_view(), name='meter_detail'),
        url(r'^logs/$',
            LogListView.as_view(), name='list_logs'),
        url(r'^meter_infos/$',
            MeterInfoListView.as_view(), name='list_meter_infos'),
        url(r'^meter_infos/create/$',
            CreateMeterInfoView.as_view(), name='create_meter_info'),
        url(r'^modes/$',
            ModeListView.as_view(), name='list_modes'),
        url(r'^modes/create/$',
            CreateModeView.as_view(), name='create_mode'),
        url(r'^accounts/login/$',
            'django.contrib.auth.views.login', name='login'),
        url(r'^accounts/logout/$',
            'django.contrib.auth.views.logout_then_login', name='logout'),
)
