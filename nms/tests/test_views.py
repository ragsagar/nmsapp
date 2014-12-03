from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

from nms.models import Tower, Well
from nms.tables import TowerTable, WellTable

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user()
        data = {'xc': 122, 'yc': 120, 'gx': 230, 'gy': 402, 'wd': 502, 'ht': 101}
        tower = self.create_tower(**data)

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
        self.client.login(username='ragsagar', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('tower', response.context_data)
        self.assertEqual(response.context_data['tower'], tower)
        self.assertTemplateUsed(response, 'nms/tower_detail.html')

    def test_tower_list(self):
        url = reverse_lazy('tower_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='ragsagar', password='password')
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
        self.client.login(username='ragsagar', password='password')
        response = self.client.get(url)
        wells = Well.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), wells.count())
        self.assertIn('table', response.context_data)
        self.assertIsInstance(response.context_data['table'], WellTable)


        
    def create_user(self, **kwargs):
        user_data = {'username': 'ragsagar', 'password': 'password'}
        user_data.update(kwargs)
        user = User.objects.create_user(**user_data)
        return user
