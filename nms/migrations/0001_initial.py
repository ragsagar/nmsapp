# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nmsrealtime', models.DateTimeField()),
                ('meterrealtime', models.DateTimeField()),
                ('modbusaddress', models.IntegerField()),
                ('index', models.IntegerField()),
                ('realdate', models.FloatField()),
                ('realtime', models.FloatField()),
                ('grandtotal', models.FloatField()),
                ('flowrate', models.FloatField()),
                ('volume', models.FloatField()),
                ('flowtime', models.FloatField()),
                ('staticpressurea', models.FloatField()),
                ('differentialpressure', models.FloatField()),
                ('corrpipesize', models.FloatField()),
                ('corrplatesize', models.FloatField()),
                ('platesize', models.FloatField()),
                ('staticpressureg', models.FloatField()),
                ('batteryvoltage', models.FloatField()),
                ('field14', models.FloatField()),
                ('field15', models.FloatField()),
                ('field16', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hourly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nmsrealtime', models.DateTimeField()),
                ('meterrealtime', models.DateTimeField()),
                ('modbusaddress', models.IntegerField()),
                ('index', models.IntegerField()),
                ('realdate', models.FloatField()),
                ('realtime', models.FloatField()),
                ('grandtotal', models.FloatField()),
                ('flowrate', models.FloatField()),
                ('volume', models.FloatField()),
                ('flowtime', models.FloatField()),
                ('staticpressurea', models.FloatField()),
                ('differentialpressure', models.FloatField()),
                ('corrpipesize', models.FloatField()),
                ('corrplatesize', models.FloatField()),
                ('platesize', models.FloatField()),
                ('staticpressureg', models.FloatField()),
                ('batteryvoltage', models.FloatField()),
                ('field14', models.FloatField()),
                ('field15', models.FloatField()),
                ('field16', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nmsrealtime', models.DateTimeField()),
                ('direction', models.IntegerField()),
                ('raw_data', models.TextField()),
                ('parsed_data', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modbusaddress', models.IntegerField(verbose_name=b'Modbus Address')),
                ('latestintervaltime', models.DateTimeField()),
                ('latesthourlytime', models.DateTimeField()),
                ('latestdailytime', models.DateTimeField()),
                ('latesthourlyindex', models.IntegerField(null=True, blank=True)),
                ('latestdailyindex', models.IntegerField(null=True, blank=True)),
                ('historicalhourlyindex', models.IntegerField(null=True, blank=True)),
                ('historicaldailyindex', models.IntegerField(null=True, blank=True)),
                ('hourlyrecords', models.IntegerField(null=True, blank=True)),
                ('dailyrecords', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeterConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modbusaddress', models.IntegerField()),
                ('registernumber', models.IntegerField(null=True, verbose_name=b'Register Number', blank=True)),
                ('registervalue', models.IntegerField(null=True, verbose_name=b'Register Value', blank=True)),
                ('dirty', models.NullBooleanField()),
                ('meter', models.ForeignKey(related_name=b'meter_configs', to='nms.Meter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeterInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.TextField()),
                ('pipeline', models.TextField()),
                ('service', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeterLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gps_lat', models.FloatField(null=True, blank=True)),
                ('gps_lon', models.FloatField(null=True, blank=True)),
                ('meter', models.ForeignKey(related_name=b'meter_location', to='nms.MeterInfo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('modename', models.TextField(serialize=False, primary_key=True)),
                ('serialport', models.TextField()),
                ('ticksperpacket', models.IntegerField()),
                ('packetsperbroadcast', models.IntegerField()),
                ('stationstatusinterval', models.IntegerField()),
                ('intervaldatainterval', models.IntegerField()),
                ('hourlydatainterval', models.IntegerField()),
                ('dailydatainterval', models.IntegerField()),
                ('maxfailedreads', models.IntegerField()),
                ('minbatt', models.IntegerField()),
                ('maxtemp', models.IntegerField()),
                ('minrssi', models.IntegerField()),
                ('maxerrors', models.IntegerField()),
                ('maxindexmatch', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nmsrealtime', models.DateTimeField()),
                ('modbusaddress', models.IntegerField()),
                ('grandtotal', models.FloatField()),
                ('flowrate', models.FloatField()),
                ('current_day_volume', models.FloatField()),
                ('static_pressure', models.FloatField()),
                ('differential_pressure', models.FloatField()),
                ('realdate', models.FloatField()),
                ('realtime', models.FloatField()),
                ('batteryvoltage', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('meter', models.ForeignKey(related_name=b'readings', to='nms.MeterInfo')),
                ('mode', models.ForeignKey(related_name=b'readings', to='nms.Mode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('stationaddress', models.IntegerField(serialize=False, verbose_name=b'Station Address', primary_key=True)),
                ('lateststatustime', models.DateTimeField(verbose_name=b'Latest Status Time')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StationLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gps_lat', models.FloatField(null=True, blank=True)),
                ('gps_lon', models.FloatField(null=True, blank=True)),
                ('stationaddress', models.ForeignKey(related_name=b'station_location', to='nms.Station')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StationStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nmsrealtime', models.DateTimeField()),
                ('rssi', models.FloatField()),
                ('batt', models.FloatField()),
                ('temp', models.FloatField()),
                ('sn', models.IntegerField()),
                ('tx', models.IntegerField()),
                ('pe', models.IntegerField()),
                ('re', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('stationaddress', models.ForeignKey(related_name=b'statuses', to='nms.Station')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reading',
            name='stationaddress',
            field=models.ForeignKey(related_name=b'readings', to='nms.Station'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meter',
            name='meter_info',
            field=models.ForeignKey(related_name=b'meters', to='nms.MeterInfo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meter',
            name='stationaddress',
            field=models.ForeignKey(related_name=b'meters', verbose_name=b'Station Address', to='nms.Station'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='meter',
            unique_together=set([('stationaddress', 'modbusaddress')]),
        ),
        migrations.AddField(
            model_name='hourly',
            name='meter',
            field=models.ForeignKey(related_name=b'hourly_readings', to='nms.MeterInfo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hourly',
            name='mode',
            field=models.ForeignKey(related_name=b'hourly_readings', to='nms.Mode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hourly',
            name='stationaddress',
            field=models.ForeignKey(related_name=b'hourly_readings', to='nms.Station'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='daily',
            name='meter',
            field=models.ForeignKey(related_name=b'daily_readings', to='nms.MeterInfo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='daily',
            name='mode',
            field=models.ForeignKey(related_name=b'daily_readings', to='nms.Mode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='daily',
            name='stationaddress',
            field=models.ForeignKey(related_name=b'daily_readings', to='nms.Station'),
            preserve_default=True,
        ),
    ]
