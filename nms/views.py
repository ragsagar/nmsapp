from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView
from django.core.urlresolvers import reverse_lazy

from django_tables2 import SingleTableView, RequestConfig
from braces.views import LoginRequiredMixin

from .models import (Station, Meter, Daily, Hourly, Reading, Log, Mode,
                     MeterInfo)
from .tables import (StationTable, MeterTable, DailyTable,
                     HourlyTable, IntervalTable, LogTable, ModeTable,
                     MeterInfoTable)


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


class ModeListView(LoginRequiredMixin, SingleTableView):
    """ View to list all Modes. """
    model = Mode
    template_name = "nms/mode_list.html"
    table_class = ModeTable


class MeterInfoListView(LoginRequiredMixin, SingleTableView):
    """ View to list all meter infos. MeterInfo with no
    associated meters will be listed as disabled. """
    model = MeterInfo
    template_name = "nms/meter_info_list.html"
    table_class = MeterInfoTable


class CreateMeterInfoView(LoginRequiredMixin, CreateView):
    """ View to create new meter info. """
    model = MeterInfo
    success_url = reverse_lazy('list_meter_infos')


class MeterInfoDetailView(LoginRequiredMixin, DetailView):
    """ View to show detail meter info. """
    model = MeterInfo
    context_object_name = 'meter_info'
    template_name = 'nms/meter_info_detail.html'


class CreateModeView(LoginRequiredMixin, CreateView):
    """ View to create new modes. """
    model = Mode
    success_url = reverse_lazy('list_modes')


class CreateStationView(LoginRequiredMixin, CreateView):
    """ View to create new station. """
    model = Station
    success_url = reverse_lazy('list_stations')


class CreateMeterView(LoginRequiredMixin, CreateView):
    """ View to create new meter. """
    model = Meter
    fields = ('stationaddress', 'modbusaddress', 'latestintervaltime',
              'latesthourlytime', 'latestdailytime', 'latesthourlyindex',
              'latestdailyindex', 'historicalhourlyindex',
              'historicaldailyindex', 'hourlyrecords', 'dailyrecords')
    
    def form_valid(self, form):
        """
        Assign the related meter info the the created meter.
        """
        self.object = form.save(commit=False)
        meter_info = get_object_or_404(MeterInfo, pk=self.kwargs.get("pk"))
        self.object.meter_info = meter_info
        self.object.save()
        return redirect(meter_info.get_absolute_url())
