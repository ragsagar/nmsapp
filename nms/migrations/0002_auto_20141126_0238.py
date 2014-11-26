# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x_coordinate', models.IntegerField()),
                ('y_coordinate', models.IntegerField()),
                ('grid_x', models.IntegerField()),
                ('grid_y', models.IntegerField()),
                ('water_depth', models.IntegerField(verbose_name=b'Water Depth(feet)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Well',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('type', models.IntegerField(default=1, choices=[(1, b'Water Injector')])),
                ('max_allowed_flowrate', models.IntegerField(verbose_name=b'Maximum Allowed Flowrate BPD')),
                ('location', models.CharField(max_length=255)),
                ('current_zone', models.CharField(max_length=255)),
                ('x_mass_tree', models.TextField()),
                ('tower', models.ForeignKey(related_name='towers', to='nms.Tower')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='meterlocation',
            name='meter',
            field=models.ForeignKey(related_name='meter_locations', to='nms.MeterInfo'),
            preserve_default=True,
        ),
    ]
