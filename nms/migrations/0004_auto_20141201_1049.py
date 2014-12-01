# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nms', '0003_auto_20141127_0251'),
    ]

    operations = [
        migrations.CreateModel(
            name='String',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('max_allowed_flowrate', models.FloatField()),
                ('number', models.IntegerField(default=1, choices=[(1, b'One'), (2, b'Two'), (3, b'Three'), (4, b'Four'), (5, b'Five'), (6, b'Six')])),
                ('well', models.ForeignKey(related_name='strings', to='nms.Well')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meterinfo',
            name='string',
            field=models.ForeignKey(related_name='meter_infos', to='nms.String', null=True),
            preserve_default=True,
        ),
    ]
