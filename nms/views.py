from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, UpdateView, View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

from django_tables2 import SingleTableView, RequestConfig
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from .models import (Station, Meter, Daily, Hourly, Reading, Log, Mode,
                     MeterInfo, StationStatus, Well, Tower)
from .tables import (StationTable, MeterTable, DailyTable,
                     HourlyTable, IntervalTable, LogTable, ModeTable,
                     MeterInfoTable, TowerTable, WellTable, UserTable)
from .utils import is_nms_running, start_nms, stop_nms
from .forms import CreateUserForm


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

    def get_context_data(self, **kwargs):
        """
        Pass the latest station status to the context.
        """

        context = super(MeterListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        station = get_object_or_404(Station, pk=pk)
        try:
            station_status = station.statuses.latest('nmsrealtime')
        except StationStatus.DoesNotExist:
            station_status = None
        context['station_status'] = station_status
        return context


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


class ModeListView(LoginRequiredMixin,
                   StaffuserRequiredMixin,
                   SingleTableView):
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
    queryset = MeterInfo.objects.all().prefetch_related('meters')


class CreateMeterInfoView(LoginRequiredMixin,
                          StaffuserRequiredMixin,
                          CreateView):
    """ View to create new meter info. """
    model = MeterInfo
    success_url = reverse_lazy('list_meter_infos')


class MeterInfoDetailView(LoginRequiredMixin, DetailView):
    """ View to show detail meter info. """
    model = MeterInfo
    context_object_name = 'meter_info'
    template_name = 'nms/meter_info_detail.html'


class CreateModeView(LoginRequiredMixin,
                     StaffuserRequiredMixin,
                     CreateView):
    """ View to create new modes. """
    model = Mode
    success_url = reverse_lazy('list_modes')


class CreateStationView(LoginRequiredMixin,
                        StaffuserRequiredMixin,
                        CreateView):
    """ View to create new station. """
    model = Station
    success_url = reverse_lazy('list_stations')


class CreateMeterView(LoginRequiredMixin,
                      StaffuserRequiredMixin,
                      CreateView):
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


class UpdateMeterInfoView(LoginRequiredMixin,
                          StaffuserRequiredMixin,
                          UpdateView):
    """ View to update meter info. """
    model = MeterInfo

    def get_success_url(self):
        return reverse_lazy('meter_info_detail',
                            kwargs={'pk': self.kwargs.get('pk')})


class ModeDetailView(LoginRequiredMixin,
                     StaffuserRequiredMixin,
                     DetailView):
    """ View to show the mode detail page. """
    model = Mode
    template_name = 'nms/mode_detail.html'


class UpdateModeView(LoginRequiredMixin,
                     StaffuserRequiredMixin,
                     UpdateView):
    """ View to update mode. """
    model = Mode

    def get_success_url(self):
        return reverse_lazy('mode_detail',
                            kwargs={'pk': self.kwargs.get('pk')})


class TowerListView(LoginRequiredMixin, SingleTableView):
    """ View to list all towers. """
    model = Tower
    table_class = TowerTable
    template_name = 'nms/tower_list.html'
    context_object_name = 'tower'


class TowerDetailView(LoginRequiredMixin, SingleTableView):
    """ View to show the detail page and table of related metes. """
    model = Well
    table_class = WellTable
    template_name = 'nms/tower_detail.html'

    def get_context_data(self, **kwargs):
        """ Pass the tower with the given pk to the context. """
        context = super(TowerDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        tower = get_object_or_404(Tower, pk=pk)
        context['tower'] = tower
        return context


class CreateTowerView(LoginRequiredMixin,
                      StaffuserRequiredMixin,
                      CreateView):
    """ View to create new tower. """
    model = Tower

    
class UpdateTowerView(LoginRequiredMixin,
                      StaffuserRequiredMixin,
                      UpdateView):
    """ View to update an existing tower. """
    model = Tower

    
class WellListView(LoginRequiredMixin, SingleTableView):
    """ View to list all wells. """
    model = Well
    table_class = WellTable
    template_name = 'nms/well_list.html'
    context_object_name = 'well'


class WellDetailView(LoginRequiredMixin, DetailView):
    """ View to show the well detail page """
    model = Well
    template_name = 'nms/well_detail.html'
    context_object_name = 'well'


class CreateWellView(LoginRequiredMixin,
                     StaffuserRequiredMixin,
                     CreateView):
    """ View to create new wells. """
    model = Well

class UpdateWellView(LoginRequiredMixin,
                     StaffuserRequiredMixin,
                     UpdateView):
    """ View to update new wells. """
    model = Well


class ControlPanelView(LoginRequiredMixin,
                       StaffuserRequiredMixin,
                       SingleTableView):
    """ View to list all logs. """
    model = Log
    template_name = "nms/control_panel.html"
    table_class = LogTable

    def get_context_data(self, **kwargs):
        """ Pass the state of nms to the context. """
        context = super(ControlPanelView, self).get_context_data(**kwargs)
        context['is_nms_running'] = is_nms_running()
        return context


class ToggleNMSView(LoginRequiredMixin,
                    StaffuserRequiredMixin,
                    View):
    """ View to toggle the state of NMS. """
    def post(self, request, *args, **kwargs):
        """ Turn NMS on if it is not running, otherwise
        start it."""
        if is_nms_running():
            stop_nms()
        else:
            start_nms()
        return redirect(reverse_lazy('control_panel'))


class UserListView(LoginRequiredMixin,
                   StaffuserRequiredMixin,
                   SingleTableView):
    model = User
    table_class = UserTable
    template_name = 'nms/user_list.html'

    
class CreateUserView(LoginRequiredMixin,
                     StaffuserRequiredMixin,
                     CreateView):
    """ View to create new users. """
    model = User
    form_class = CreateUserForm
    template_name = 'nms/user_form.html'
    success_url = reverse_lazy('user_list')
    fields = ('username', 'is_active', 'is_staff')
        
