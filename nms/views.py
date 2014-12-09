from datetime import timedelta
from dateutil import rrule
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (DetailView, CreateView, UpdateView, View,
                                  FormView, TemplateView)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone

from django_tables2 import SingleTableView, RequestConfig
from braces.views import (LoginRequiredMixin, StaffuserRequiredMixin,
                          JSONResponseMixin)

from .models import (Station, Meter, Daily, Hourly, Reading, Log, Mode,
                     MeterInfo, StationStatus, Well, Tower, String)
from .tables import (StationTable, MeterTable, DailyTable,
                     HourlyTable, IntervalTable, LogTable, ModeTable,
                     MeterInfoTable, TowerTable, WellTable, UserTable)
from .utils import is_nms_running, start_nms, stop_nms
from .forms import CreateUserForm, WellForm


class DashboardView(LoginRequiredMixin, TemplateView):
    """ View to render a dashbord template. """
    template_name = 'nms/dashbord.html'
    

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
        interval_readings = Reading.objects.filter(meter__meters=meter).order_by('nmsrealtime')
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

    def get_context_data(self, **kwargs):
        """
        if meter is present we are showing the meter detail in
        the same page.
        """
        context_data = super(MeterInfoDetailView, self
                                    ).get_context_data(**kwargs)
        config = RequestConfig(self.request)
        meter = self.object.related_meter
        if meter:
            daily_readings = Daily.objects.filter(meter__meters=meter)
            daily_table = DailyTable(daily_readings, prefix='daily-')
            config.configure(daily_table)
            hourly_readings = Hourly.objects.filter(meter__meters=meter)
            hourly_table = HourlyTable(hourly_readings, prefix='hourly-')
            config.configure(hourly_table)
            interval_readings = Reading.objects.filter(meter__meters=meter)
            interval_table = IntervalTable(interval_readings, prefix='inv-')
            config.configure(interval_table)
            context_data.update({'daily_table': daily_table,
                                 'hourly_table': hourly_table,
                                 'interval_table': interval_table})


        return context_data


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
    fields = ('name', 'x_coordinate', 'y_coordinate',
              'grid_x', 'grid_y', 'water_depth', 'helideck_height')

    
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
    fields = ('name', 'slot', 'type', 'string',
              'max_allowed_flowrate', 'location',
              'current_zone', 'xmas_tree', 'tower')

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


class UserDetailView(LoginRequiredMixin,
                     StaffuserRequiredMixin,
                     DetailView):
    """ View to show user detail page. """
    model = User
    template_name = 'nms/user_detail.html'
    context_object_name = 'user_obj'
        

class ChangeMyPasswordView(LoginRequiredMixin,
                           FormView):
    """ View to change one's own password. """
    model = User
    template_name = 'nms/user_form.html'
    success_url = reverse_lazy('list_stations')
    form_class = PasswordChangeForm

    def form_valid(self, form):
        """ Save the form if it is valid. """
        form.save()
        return redirect(self.get_success_url())
        

    def get_form_kwargs(self):
        """ Pass the currently loggen in user to the form init."""
        kwargs = super(ChangeMyPasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CreateStringView(LoginRequiredMixin,
                       CreateView):
    """ View to add strings to wells. """
    model = String
    fields = ('max_allowed_flowrate', 'number')

    def form_valid(self, form):
        """ Get the pk from the url and save the well 
        with that pk as related well. """
        self.object = form.save(commit=False)
        pk = self.kwargs.get('pk')
        well = get_object_or_404(Well, pk=pk)
        self.object.well = well
        self.object.save()
        return redirect(well.get_absolute_url())


class GetStringsJSONView(LoginRequiredMixin,
                         JSONResponseMixin,
                         View):
    """ View to fetch the list of all strings
    of a well. """
    def get(self, request, *args, **kwargs):
        """ Return the list of list of string 
        number and it's pk as json. """
        form = WellForm(request.GET)
        if form.is_valid():
            well = form.cleaned_data.get('well')
            strings = well.strings.all().only('number')
            response = []
            for string in strings:
                response.append({'pk': string.pk,
                                 'number': string.get_number_display()})
        else:
            response = []
        return self.render_json_response(response)

class GetDashboardWidgetJOSONView(LoginRequiredMixin,
                                  JSONResponseMixin,
                                  View):
    """ View to returns a json data of reading in the
    dashboard """
    def get(self, request):
        today = timezone.now()
        yester_day = today.date() - timedelta(days=1)
        towers = Tower.objects.all()
        wells = Well.objects.all()
        todays_reading = Reading.objects.filter(nmsrealtime__year=today.year,
                                                nmsrealtime__month=today.month,
                                                nmsrealtime__day=today.day
                                                ).order_by('-nmsrealtime')

        yesterdays_reading = Reading.objects.filter(
                                                nmsrealtime__year=yester_day.year,
                                                nmsrealtime__month=yester_day.month,
                                                nmsrealtime__day=yester_day.day
                                                ).order_by('-nmsrealtime')
        today_total_reading = None
        yesterdays_total_reading = None
        if todays_reading:
            today_total_reading = todays_reading[0].current_day_volume
        if yesterdays_reading:
            yesterdays_total_reading = yesterdays_reading[0].current_day_volume
        # Construction data of volume per date.
        # looping all meter and find each day reading and taking the last 
        # value injected.
        # we are only loop 15 days past to show the days volume chart,
        meters = MeterInfo.objects.all()
        meter_chart_data = []
        thirty_days_past_date = today.date() - timedelta(days=15)
        labels=['x']
        for current_date in rrule.rrule(rrule.DAILY, dtstart=thirty_days_past_date, until=today.date()):
            labels.append(current_date.date())
        meter_chart_data.append(labels)
        for meter in meters:
            data_list = [meter.tag]
            for current_date in rrule.rrule(rrule.DAILY, dtstart=thirty_days_past_date, until=today.date()):
                readings = meter.readings.filter(nmsrealtime__day=current_date.day,
                                                 nmsrealtime__month=current_date.month,
                                                 nmsrealtime__year=current_date.year).order_by('-nmsrealtime')
                if readings:
                    data_list.append(readings[0].current_day_volume)
            meter_chart_data.append(data_list)
        # Showing the todays reading in all well.
        # Looping through all well and aggrigate total reading 
        # return labls and values we constructon as js expecting.
        well_chart_data = ['Total Injection Today']
        well_labels =[]
        for well in wells:
            well_labels.append(well.name)
            well_total_reading = 0
            for meter in well.meter_infos.all():
                date = today.date() - timedelta(days=1)
                todays_reading = meter.readings.filter(nmsrealtime__day=date.day,
                                                       nmsrealtime__month=date.month,
                                                       nmsrealtime__year=date.year
                                                ).order_by('-nmsrealtime')
                if todays_reading:
                    well_total_reading += todays_reading[0].current_day_volume
            well_chart_data.append(well_total_reading)
        well_data = {
            'chart_data': well_chart_data,
            'well_labels': well_labels,
        }

        response = {
            'tower_count': towers.count(),
            'well_cont': wells.count(),
            'todays_reading': today_total_reading,
            'yesterdays_total_reading': yesterdays_total_reading,
            'meter_chart_data': meter_chart_data,
            'well_chart_data': well_data,
        }

        return self.render_json_response(response)

# class GetReadingByDaysJSONView(LoginRequiredMixin,
#                                JSONResponseMixin,
#                                View):
#     """ View returs a json data with reading by each data """
    

            
