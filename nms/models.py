from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.utils.functional import cached_property

from model_utils import Choices


class Tower(models.Model):
    name = models.CharField(max_length=255)
    x_coordinate = models.IntegerField(verbose_name='X Coordinates(UTM)')
    y_coordinate = models.IntegerField(verbose_name='Y Coordinates(UTM)')
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()
    water_depth = models.IntegerField(verbose_name="Water Depth(feet)")
    helideck_height = models.IntegerField(
                             verbose_name='Helideck Height(feets)')

    def get_absolute_url(self):
        return reverse_lazy('tower_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"%s - %s" % (self.x_coordinate, self.y_coordinate)


class Well(models.Model):
    TYPES = Choices(
        (1, 'water_injector', 'Water Injector'),
        )
    SLOTS = Choices(
        (1, 'one', 'One'),
        (2, 'two', 'Two'),
        (3, 'three', 'Three'),
        (4, 'four', 'Four'),
        (5, 'five', 'Five'),
        (6, 'six', 'Six'),
        (7, 'seven', 'Seven'),
        (8, 'eight', 'Eight'),
        (9, 'nine', 'Nine'),
        )
    STRINGS = Choices(
        (1, 'one', 'One'),
        (2, 'two', 'Two'),
        (3, 'three', 'Three'),
        (4, 'four', 'Four'),
        (5, 'five', 'Five'),
        (6, 'six', 'Six'),
        )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    slot = models.IntegerField(choices=SLOTS, default=SLOTS.one)
    type = models.IntegerField(choices=TYPES, default=TYPES.water_injector)
    string = models.IntegerField(choices=STRINGS, default=STRINGS.one)
    max_allowed_flowrate = models.IntegerField(
                            verbose_name="Maximum Allowed Flowrate BPD")
    location = models.CharField(max_length=255)
    current_zone = models.CharField(max_length=255)
    xmas_tree = models.CharField(max_length=255)
    tower = models.ForeignKey(Tower, related_name='towers')

    def get_absolute_url(self):
        return reverse_lazy('well_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"%s - %s" % (self.location, self.current_zone)

    
class Station(models.Model):
    stationaddress = models.IntegerField(primary_key=True,
                                         verbose_name='Station Address')
    lateststatustime = models.DateTimeField(verbose_name='Latest Status Time')
    tower = models.ForeignKey(Tower, null=True, related_name='stations')

    def __unicode__(self):
        return u"%s" % self.stationaddress


class StationStatus(models.Model): 
    stationaddress = models.ForeignKey(Station, related_name='statuses')
    nmsrealtime = models.DateTimeField()
    rssi = models.FloatField()
    batt = models.FloatField()
    temp = models.FloatField()
    sn = models.IntegerField()
    tx = models.IntegerField()
    pe = models.IntegerField()
    re = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    
class String(models.Model):
    STRINGS = Choices(
        (1, 'one', 'One'),
        (2, 'two', 'Two'),
        (3, 'three', 'Three'),
        (4, 'four', 'Four'),
        (5, 'five', 'Five'),
        (6, 'six', 'Six'),
        )
    created = models.DateTimeField(auto_now_add=True)
    max_allowed_flowrate = models.FloatField()
    number = models.IntegerField(choices=STRINGS,
                                 default=STRINGS.one)
    well = models.ForeignKey(Well, related_name='strings')

    def __unicode__(self):
        return self.get_number_display()


class MeterInfo(models.Model):
    tag = models.TextField()
    pipeline = models.TextField()
    service = models.TextField()
    well = models.ForeignKey(Well,
                             related_name='meter_infos',
                             null=True)
    string = models.ForeignKey(String,
                               related_name='meter_infos',
                               null=True)

    @cached_property
    def related_meter(self):
        """ Return related meter if it exists. """
        meters = self.meters.all()
        if meters:
            return meters[0]
        else:
            return None

    def get_absolute_url(self):
        return reverse_lazy('meter_info_detail',
                            kwargs={'pk': self.pk})

    @cached_property
    def related_location(self):
        """ Return related meter if it exists. """
        locations = self.meter_locations.all()
        if locations:
            return locations[0]
        else:
            return None


class Meter(models.Model):
    stationaddress = models.ForeignKey(Station, related_name='meters',
                                       verbose_name='Station Address')
    modbusaddress = models.IntegerField(verbose_name='Modbus Address')
    latestintervaltime = models.DateTimeField()
    latesthourlytime = models.DateTimeField()
    latestdailytime = models.DateTimeField()
    latesthourlyindex = models.IntegerField(blank=True, null=True)
    latestdailyindex = models.IntegerField(blank=True, null=True)
    historicalhourlyindex  = models.IntegerField(blank=True, null=True)
    historicaldailyindex  = models.IntegerField(blank=True, null=True)
    hourlyrecords  = models.IntegerField(blank=True, null=True)
    dailyrecords  = models.IntegerField(blank=True, null=True)
    meter_info = models.ForeignKey(MeterInfo, related_name='meters')
    well = models.ForeignKey(Well, related_name='meters', null=True)

    def get_absolute_url(self):
        return reverse_lazy('meter_detail',
                            kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"%s %s" % (self.stationaddress, self.modbusaddress)

    class Meta:
        unique_together = ('stationaddress', 'modbusaddress')


class MeterConfig(models.Model):
    meter = models.ForeignKey(Meter, related_name='meter_configs')
    modbusaddress = models.IntegerField()
    registernumber = models.IntegerField(blank=True, null=True,
                                         verbose_name='Register Number')
    registervalue = models.IntegerField(blank=True, null=True,
                                        verbose_name='Register Value')
    dirty = models.NullBooleanField()

    def __unicode__(self):
        return u"%s" % (self.modbusaddress)


class Mode(models.Model):
    modename = models.TextField(primary_key=True)
    serialport = models.TextField()
    ticksperpacket = models.IntegerField()
    packetsperbroadcast = models.IntegerField()
    stationstatusinterval = models.IntegerField()
    intervaldatainterval = models.IntegerField()
    hourlydatainterval = models.IntegerField()
    dailydatainterval = models.IntegerField()
    maxfailedreads = models.IntegerField()
    minbatt = models.IntegerField()
    maxtemp = models.IntegerField()
    minrssi = models.IntegerField()
    maxerrors = models.IntegerField()
    maxindexmatch = models.IntegerField()


class Daily(models.Model):   
    nmsrealtime = models.DateTimeField()
    meterrealtime = models.DateTimeField()
    stationaddress = models.ForeignKey(Station, related_name='daily_readings')
    modbusaddress = models.IntegerField()
    meter = models.ForeignKey(MeterInfo, related_name='daily_readings')
    mode = models.ForeignKey(Mode, related_name='daily_readings')
    #stationaddress = models.IntegerField()
    #modbusid = models.IntegerField()
    index = models.IntegerField()
    realdate = models.FloatField()
    realtime = models.FloatField()
    grandtotal = models.FloatField()
    flowrate = models.FloatField()
    volume = models.FloatField()
    flowtime = models.FloatField()
    staticpressurea= models.FloatField()
    differentialpressure = models.FloatField()
    corrpipesize = models.FloatField()
    corrplatesize = models.FloatField()
    platesize = models.FloatField()
    staticpressureg = models.FloatField()
    batteryvoltage = models.FloatField()
    field14 = models.FloatField()
    field15 = models.FloatField()
    field16 = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)


class Hourly(models.Model):
    nmsrealtime = models.DateTimeField()
    meterrealtime = models.DateTimeField()
    #stationaddress = models.IntegerField()
    #modbusid = models.IntegerField()
    stationaddress = models.ForeignKey(Station, related_name='hourly_readings')
    modbusaddress = models.IntegerField()
    meter = models.ForeignKey(MeterInfo, related_name='hourly_readings')
    mode = models.ForeignKey(Mode, related_name='hourly_readings')
    index = models.IntegerField()
    realdate = models.FloatField()
    realtime = models.FloatField()
    grandtotal = models.FloatField()
    flowrate = models.FloatField()
    volume = models.FloatField()
    flowtime = models.FloatField()
    staticpressurea= models.FloatField()
    differentialpressure = models.FloatField()
    corrpipesize = models.FloatField()
    corrplatesize = models.FloatField()
    platesize = models.FloatField()
    staticpressureg = models.FloatField()
    batteryvoltage = models.FloatField()
    field14 = models.FloatField()
    field15 = models.FloatField()
    field16 = models.FloatField()
    created = models.DateTimeField(auto_now_add=True) # this will be autopopulated with current machine time
    


class Reading(models.Model):
    nmsrealtime = models.DateTimeField()
    #modbusid = models.IntegerField()
    stationaddress = models.ForeignKey(Station, related_name='readings')
    modbusaddress = models.IntegerField()
    meter = models.ForeignKey(MeterInfo, related_name='readings')
    mode = models.ForeignKey(Mode, related_name='readings') 
    grandtotal = models.FloatField()
    flowrate = models.FloatField()
    current_day_volume = models.FloatField()
    static_pressure = models.FloatField()
    differential_pressure = models.FloatField()
    realdate = models.FloatField()
    realtime = models.FloatField()
    batteryvoltage = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    

class Log(models.Model):
    nmsrealtime = models.DateTimeField()
    direction = models.IntegerField()
    raw_data = models.TextField()
    parsed_data = models.TextField()


class MeterLocation(models.Model):
    meter = models.ForeignKey(MeterInfo, related_name='meter_locations')
    gps_lat = models.FloatField(blank=True, null=True)
    gps_lon = models.FloatField(blank=True, null=True)


class StationLocation(models.Model):
    stationaddress = models.ForeignKey(Station,
                                       related_name='station_location')
    gps_lat = models.FloatField(blank=True, null=True)
    gps_lon = models.FloatField(blank=True, null=True)

    
