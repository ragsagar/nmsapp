from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.utils import timezone

from nms.models import Tower, Well, Station, StationStatus, Meter, MeterInfo, String, Mode
from nms.tables import (TowerTable, WellTable, StationTable, MeterTable,
                        DailyTable, HourlyTable, IntervalTable, ModeTable)

class ViewTest(TestCase):
    def setUp(self):
        self.credentials = {'username': 'ragsagar',
                            'password': 'password',}
        self.client = Client()
        self.user = self.create_user()
        data = {'xc': 122, 'yc': 120, 'gx': 230, 'gy': 402, 'wd': 502, 'ht': 101}
        tower = self.create_tower(**data)
        well = Well.objects.create(name="Well1", slot=Well.SLOTS.one,
                                   type=Well.TYPES.water_injector, string=Well.STRINGS.one,
                                   max_allowed_flowrate=10, location='UAE', current_zone='Dubai',
                                   xmas_tree='Valtek', tower=tower)
        station = Station.objects.create(stationaddress=123,
                                         lateststatustime=timezone.now(),
                                         tower=tower)
        station_status = StationStatus.objects.create(stationaddress=station,
                                                      nmsrealtime=timezone.now(),
                                                      rssi=20, batt=30, temp=90, sn=23,
                                                      tx=30, pe=44, re=23)
        string = String.objects.create(max_allowed_flowrate=20,
                                       number=String.STRINGS.one,
                                       well=well)
        meter_info = MeterInfo.objects.create(tag="Tag1",
                                              pipeline="Pipeline1",
                                              service="Service1",
                                              well=well,
                                              string=string)
        meter = Meter.objects.create(stationaddress=station,
                                     modbusaddress="23",
                                     latestintervaltime=timezone.now(),
                                     latesthourlytime=timezone.now(),
                                     latestdailytime=timezone.now(),
                                     meter_info=meter_info,
                                     well=well)
        mode_data = {'modename': u'mode2', 'maxerrors': 45, 'maxtemp': 2,
                     'stationstatusinterval': 123, 'maxindexmatch': 45,
                     'minbatt': 34, 'serialport': u'sp1',
                     'dailydatainterval': 34, 'minrssi': 49,
                     'intervaldatainterval': 2, 'ticksperpacket': 23,
                     'packetsperbroadcast': 12, 'hourlydatainterval': 3,
                     'maxfailedreads': 23}
        mode = Mode.objects.create(**mode_data)

        
    def create_user(self, **kwargs):
        user_data = self.credentials
        user_data.update(kwargs)
        user = User.objects.create_user(**user_data)
        user.is_staff = True
        user.save()
        return user

    def create_tower(self, xc, yc, gx, gy, wd, ht):
        data = {'y_coordinate': yc,
                'grid_x': gx,
                'water_depth': wd,
                'x_coordinate': xc,
                'grid_y': gy,
                'helideck_height': ht
        }
        return Tower.objects.create(**data)

    def test_stations_list(self):
        url = reverse('list_stations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        stations = Station.objects.all()
        self.assertEqual(len(response.context_data['object_list']), stations.count())
        self.assertTemplateUsed(response, 'nms/station_list.html')
        self.assertIn('table', response.context_data)
        self.assertIsInstance(response.context_data['table'], StationTable)

    def test_station_meter_listing(self):
        station = Station.objects.all()[0]
        url = reverse('station_meters_list', kwargs={'pk': station.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('station_status', response.context_data)
        self.assertEqual(response.context_data['station_status'],
                         station.statuses.latest('nmsrealtime'))
        self.assertTemplateUsed(response, 'nms/meter_list.html')
        self.assertIn('table', response.context_data)
        self.assertIsInstance(response.context_data['table'], MeterTable)

    def test_meter_detail(self):
        meter = Meter.objects.all()[0]
        url = reverse('meter_detail', kwargs={'pk': meter.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('meter', response.context_data)
        self.assertIsInstance(response.context_data['meter'], Meter)
        self.assertIsInstance(response.context_data['daily_table'], DailyTable)
        self.assertIsInstance(response.context_data['hourly_table'], HourlyTable)
        self.assertIsInstance(response.context_data['interval_table'], IntervalTable)
        self.assertTemplateUsed(response, 'nms/meter_detail.html')

    def test_mode_list(self):
        url = reverse('list_modes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        modes = Mode.objects.all()
        self.assertEqual(len(response.context_data['object_list']), modes.count())
        self.assertTemplateUsed(response, 'nms/mode_list.html')
        self.assertIsInstance(response.context_data['table'], ModeTable)

    def test_mode_detail(self):
        mode = Mode.objects.all()[0]
        url = reverse('mode_detail', kwargs={'pk': mode.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.context_data['mode'], mode)
        self.assertTemplateUsed(response, 'nms/mode_detail.html')

    def test_create_mode(self):
        url = reverse('create_mode')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)
        self.assertTemplateUsed(response, 'nms/mode_form.html')
        old_count = int(Mode.objects.all().count())
        data = {'modename': u'mode3', 'maxerrors': 4,
                'maxtemp': 22, 'stationstatusinterval': 13,
                'maxindexmatch': 45, 'minbatt': 34,
                'serialport': u'sp1', 'dailydatainterval': 34,
                'minrssi': 49, 'intervaldatainterval': 2,
                'ticksperpacket': 23, 'packetsperbroadcast': 12,
                'hourlydatainterval': 3, 'maxfailedreads': 23}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Mode.objects.all().count(), old_count+1)
       
    def test_tower_detail(self):
        data = {'xc': 10, 'yc': 20, 'gx': 30, 'gy': 40, 'wd': 50, 'ht': 10}
        tower = self.create_tower(**data)
        url = reverse_lazy('tower_detail', kwargs={'pk': tower.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('tower', response.context_data)
        self.assertEqual(response.context_data['tower'], tower)
        self.assertTemplateUsed(response, 'nms/tower_detail.html')

    def test_tower_list(self):
        url = reverse_lazy('tower_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        towers = Tower.objects.all()
        self.assertEqual(len(response.context_data['object_list']), towers.count())
        self.assertTemplateUsed(response, 'nms/tower_list.html')
        self.assertIn('table', response.context_data)
        self.assertIsInstance(response.context_data['table'], TowerTable)

    def test_create_tower_view(self):
        url = reverse('create_tower')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nms/tower_form.html')
        old_count = int(Tower.objects.all().count())
        data = {'y_coordinate': 100,
                'grid_x': 200,
                'water_depth': 201,
                'x_coordinate': 203,
                'grid_y': 223,
                'helideck_height': 233,
                'name': 'Tower2',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tower.objects.all().count(), old_count+1)

    def test_update_tower_view(self):
        tower = Tower.objects.all()[0]
        url = reverse('update_tower', kwargs={'pk': tower.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nms/tower_form.html')
        self.assertIn('form', response.context_data)
        data = {'y_coordinate': 100,
                'grid_x': 300,
                'water_depth': 20,
                'x_coordinate': 203,
                'grid_y': 200,
                'helideck_height': 100,
                'name': 'EditedTower',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, str(tower.get_absolute_url()))
        updated_tower = Tower.objects.get(pk=tower.pk)
        self.assertEqual(updated_tower.name, 'EditedTower')
        self.assertEqual(updated_tower.grid_y, 200)

        
    def test_well_list(self):
        url = reverse_lazy('well_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        wells = Well.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), wells.count())
        self.assertIn('table', response.context_data)
        self.assertIsInstance(response.context_data['table'], WellTable)

    def test_well_detail(self):
        well = Well.objects.all()[0]
        url = reverse_lazy('well_detail', kwargs={'pk': well.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('well', response.context_data)
        self.assertEqual(response.context_data['well'], well)
        self.assertTemplateUsed(response, 'nms/well_detail.html')

    def test_create_well_view(self):
        url = reverse('create_well')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nms/well_form.html')
        old_count = int(Well.objects.all().count())
        data = dict(name="Well2", slot=Well.SLOTS.one,
                    type=Well.TYPES.water_injector, string=Well.STRINGS.one,
                    max_allowed_flowrate=10, location='UAE', current_zone='Dubai',
                    xmas_tree='Well', tower=Tower.objects.all()[0].pk)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Well.objects.all().count(), old_count+1)
