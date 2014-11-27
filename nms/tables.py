from django.contrib.auth.models import User

import django_tables2 as tables

from .models import (Station, Meter, Hourly, Daily, Reading, Log,
                     Mode, MeterInfo, Well, Tower)


class StationTable(tables.Table):
    stationaddress = tables.LinkColumn('station_meters_list',
                                       args=[tables.utils.A('pk')],
                                       )
    class Meta:
        model = Station
        attrs = {'class': "table table-striped table_condensed rowlink",
                 'data-link': 'row'}
        per_page = 10


class MeterTable(tables.Table):
    modbusaddress = tables.LinkColumn('meter_detail',
                                       args=[tables.utils.A('pk')],
                                       )
    tag = tables.Column(accessor='meter_info.tag')
    pipeline = tables.Column(accessor='meter_info.pipeline')
    service = tables.Column(accessor='meter_info.service')

    class Meta:
        model = Meter
        fields = ('id', 'stationaddress', 'modbusaddress')
        attrs = {'class': "table table-condensed rowlink",
                 'data-link': 'row'}


class IntervalTable(tables.Table):
    class Meta:
        model = Reading
        attrs = {'class': 'table table-condensed'}
        exclude = ('stationaddress', 'modbusaddress',
                   'meter', 'mode', 'meterrealtime', 'index',
                   'field14', 'field15', 'field16', 'created', 'id')


class HourlyTable(tables.Table):
    class Meta:
        model = Hourly
        attrs = {'class': 'table table-condensed'}
        exclude = ('stationaddress', 'modbusaddress',
                   'meter', 'mode', 'id', 'field14', 'field15', 'field16',
                   'created', 'index', 'realdate', 'realtime',
                   'meterrealtime')


class DailyTable(tables.Table):
    class Meta:
        model = Daily
        attrs = {'class': 'table table-condensed'}
        exclude = ('stationaddress', 'modbusaddress',
                   'meter', 'mode', 'meterrealtime', 'index',
                   'field14', 'field15', 'field16', 'created', 'id',
                   'realdate', 'realtime')


class LogTable(tables.Table):
    class Meta:
        model = Log
        attrs = {'class': 'table table-condensed'}


class ModeTable(tables.Table):
    modename = tables.LinkColumn('mode_detail',
                                 args=[tables.utils.A('pk')],
                                )
    class Meta:
        model = Mode
        fields = ('modename', 'serialport', 'ticksperpacket',
                  'packetsperbroadcast', 'minbatt', 'maxtemp')
        attrs = {'class': "table table-condensed rowlink",
                 'data-link': 'row'}


class MeterInfoTable(tables.Table):
    id = tables.LinkColumn('meter_info_detail',
                           args=[tables.utils.A('pk')])
    meter = tables.Column(accessor='related_meter.modbusaddress')
    class Meta:
        model = MeterInfo
        attrs = {'class': "table table-condensed rowlink",
                 'data-link': 'row'}


class TowerTable(tables.Table):
    id = tables.LinkColumn('tower_detail',
                           args=[tables.utils.A('pk')])
    class Meta:
        model = Tower
        attrs = {'class': "table table-condensed rowlink",
                 'data-link': 'row'}


class WellTable(tables.Table):
    id = tables.LinkColumn('well_detail',
                           args=[tables.utils.A('pk')])
    class Meta:
        model = Well
        attrs = {'class': "table table-condensed rowlink",
                 'data-link': 'row'}

        
class UserTable(tables.Table):
    id = tables.LinkColumn('user_detail',
                           args=[tables.utils.A('pk')])
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'date_joined')
        attrs = {'class': "table table-condensed rowlink",
                 'data-link': 'row'}


