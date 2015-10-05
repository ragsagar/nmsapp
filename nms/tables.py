from django.contrib.auth.models import User

import django_tables2 as tables

from .models import (Station, Meter, Hourly, Daily, Reading, Log,
                     Mode, MeterInfo, Well, Tower)


class StationTable(tables.Table):
    stationaddress = tables.LinkColumn('station_meters_list',
                                       args=[tables.utils.A('pk')],
                                       )
    rssi = tables.Column(accessor="latest_status.rssi")
    batt = tables.Column(accessor="latest_status.batt")
    temp = tables.Column(accessor="latest_status.temp")

    class Meta:
        model = Station
        attrs = {'class': "table table-bordered table-hover table_condensed rowlink",
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
        fields = ('id', 'modbusaddress')
        attrs = {'class': "table table-condensed table-hover table-bordered rowlink",
                 'data-link': 'row'}


class IntervalTable(tables.Table):
    flowrate = tables.Column("Flowrate (bbl/d)", accessor="flowrate_in_barrels")
    class Meta:
        model = Reading
        attrs = {'class': 'table table-condensed table-hover table-bordered'}
        exclude = ('stationaddress', 'modbusaddress',
                   'meter', 'mode', 'meterrealtime', 'index',
                   'field14', 'field15', 'field16', 'created', 'id',
                   'realdate', 'realtime',)


class HourlyTable(tables.Table):
    flowrate = tables.Column("Flowrate (bbl/d)", accessor="flowrate_in_barrels")
    class Meta:
        model = Hourly
        attrs = {'class': 'table table-condensed table-hover table-bordered'}
        exclude = ('stationaddress', 'modbusaddress',
                   'meter', 'mode', 'id', 'field14', 'field15', 'field16',
                   'created', 'index', 'realdate', 'realtime',
                   'meterrealtime', 'staticpressureg')


class DailyTable(tables.Table):
    flowrate = tables.Column("Flowrate (bbl/d)", accessor="flowrate_in_barrels")

    class Meta:
        model = Daily
        attrs = {'class': 'table table-condensed table-hover table-bordered'}
        exclude = ('stationaddress', 'modbusaddress',
                   'meter', 'mode', 'meterrealtime', 'index',
                   'field14', 'field15', 'field16', 'created', 'id',
                   'realdate', 'realtime', 'staticpressureg')


class LogTable(tables.Table):
    class Meta:
        model = Log
        attrs = {'class': 'table table-condensed table-hover table-bordered'}


class ModeTable(tables.Table):
    modename = tables.LinkColumn('mode_detail',
                                 args=[tables.utils.A('pk')],
                                )
    class Meta:
        model = Mode
        fields = ('modename', 'serialport', 'ticksperpacket',
                  'packetsperbroadcast', 'minbatt', 'maxtemp')
        attrs = {'class': "table table-condensed table-hover table-bordered rowlink",
                 'data-link': 'row'}


class MeterInfoTable(tables.Table):
    id = tables.LinkColumn('meter_info_detail',
                           args=[tables.utils.A('pk')])
    meter = tables.Column(accessor='related_meter.modbusaddress')
    # table head class name conflict with bootstrap well
    # So pass the well as hidden and add new well1 for showing in the 
    # table
    well = tables.Column(visible=False)
    well1 = tables.Column(accessor='well')
    modbus_address = tables.Column(accessor="related_meter.modbusaddress")
    station_address = tables.Column(accessor="related_meter.stationaddress")

    class Meta:
        model = MeterInfo
        attrs = {'class': "table table-condensed table-hover table-bordered rowlink",
                 'data-link': 'row'}


class TowerTable(tables.Table):
    id = tables.LinkColumn('tower_detail',
                           args=[tables.utils.A('pk')])
    class Meta:
        model = Tower
        attrs = {'class': "table table-condensed table-hover table-bordered rowlink",
                 'data-link': 'row'}


class WellTable(tables.Table):
    id = tables.LinkColumn('well_detail',
                           args=[tables.utils.A('pk')])
    class Meta:
        model = Well
        attrs = {'class': "table table-condensed table-hover table-bordered rowlink",
                 'data-link': 'row'}

        
class UserTable(tables.Table):
    id = tables.LinkColumn('user_detail',
                           args=[tables.utils.A('pk')])
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'date_joined')
        attrs = {'class': "table table-condensed table-hover table-bordered rowlink",
                 'data-link': 'row'}


