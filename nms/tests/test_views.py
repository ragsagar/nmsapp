from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

from nms.models import Tower

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user()

    def create_tower(self, xc, yc, gx, gy, wd):
        data = {'y_coordinate': yc,
                'grid_x': gx,
                'water_depth': wd,
                'x_coordinate': xc,
                'grid_y': gy}
        return Tower.objects.create(**data)
        

    def test_tower_list(self):
        url = reverse_lazy('tower_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='ragsagar', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_well_list(self):
        url = reverse_lazy('well_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='ragsagar', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_tower_detail(self):
        data = {'xc': 10, 'yc': 20, 'gx': 30, 'gy': 40, 'wd': 50}
        tower = self.create_tower(**data)
        url = reverse_lazy('tower_detail', kwargs={'pk': tower.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='ragsagar', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        
    def create_user(self, **kwargs):
        user_data = {'username': 'ragsagar', 'password': 'password'}
        user_data.update(kwargs)
        user = User.objects.create_user(**user_data)
        return user
