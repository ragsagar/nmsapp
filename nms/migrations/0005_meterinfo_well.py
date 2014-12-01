# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nms', '0004_auto_20141201_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='meterinfo',
            name='well',
            field=models.ForeignKey(related_name='meter_infos', to='nms.Well', null=True),
            preserve_default=True,
        ),
    ]
