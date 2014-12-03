from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import User

from nms.models import Tower, Well
from nms.tables import TowerTable, WellTable

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
        old_count = Well.objects.all().count()
        data = dict(name="Well2", slot=Well.SLOTS.one,
                    type=Well.TYPES.water_injector, string=Well.STRINGS.one,
                    max_allowed_flowrate=10, location='UAE', current_zone='Dubai',
                    xmas_tree='Well', tower=Tower.objects.all()[0])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Well.objects.all().count(), old_count)
