from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from django_tables2 import SingleTableView, RequestConfig
from braces.views import LoginRequiredMixin

from .models import Station, Meter, Daily, Hourly, Reading, Log
from .tables import (StationTable, MeterTable, DailyTable,
                     HourlyTable, IntervalTable, LogTable)


class StationListView(LoginRequiredMixin, SingleTableView):
    """ View to list all stations. """
    model = Station
    table_class = StationTable
    template_name = "nms/station_list.html"


class MeterListView(LoginRequiredMixin, SingleTableView):
    """ View to list all meters. """
    model = Meter
    table_class = MeterTable
    template_name = "nms/meter_list.html"

    def get_queryset(self):
        """
        List the meters for the selected station.
        """
        queryset = super(MeterListView, self).get_queryset()
        pk = self.kwargs.get('pk')
        station = get_object_or_404(Station, pk=pk)
        queryset = queryset.filter(stationaddress=station)
        return queryset


class MeterDetailView(LoginRequiredMixin, DetailView):
    """ View to see the all th readings of the meter """
    model = Meter
    template_name = "nms/meter_detail.html"

    def get_context_data(self, **kwargs):
        """ Show tables for each readings. """
        context = super(MeterDetailView, self).get_context_data(**kwargs)
        config = RequestConfig(self.request)
        meter = self.object
        daily_readings = Daily.objects.filter(meter__meters=meter)
        daily_table = DailyTable(daily_readings, prefix='daily-')
        config.configure(daily_table)
        hourly_readings = Hourly.objects.filter(meter__meters=meter)
        hourly_table = HourlyTable(hourly_readings, prefix='hourly-')
        config.configure(hourly_table)
        interval_readings = Reading.objects.filter(meter__meters=meter)
        interval_table = IntervalTable(interval_readings, prefix='inv-')
        config.configure(interval_table)
        context.update({'daily_table': daily_table,
                        'hourly_table': hourly_table,
                        'interval_table': interval_table})
        return context


class LogListView(LoginRequiredMixin, SingleTableView):
    """ View to list all logs. """
    model = Log
    template_name = "nms/log_list.html"
    table_class = LogTable

