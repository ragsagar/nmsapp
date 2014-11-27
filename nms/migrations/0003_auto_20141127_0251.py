# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nms', '0002_auto_20141126_0238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='well',
            name='x_mass_tree',
        ),
        migrations.AddField(
            model_name='meter',
            name='well',
            field=models.ForeignKey(related_name='meters', to='nms.Well', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='station',
            name='tower',
            field=models.ForeignKey(related_name='stations', to='nms.Tower', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tower',
            name='helideck_height',
            field=models.IntegerField(default=0, verbose_name=b'Helideck Height(feets)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tower',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='well',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='well',
            name='slot',
            field=models.IntegerField(default=1, choices=[(1, b'One'), (2, b'Two'), (3, b'Three'), (4, b'Four'), (5, b'Five'), (6, b'Six'), (7, b'Seven'), (8, b'Eight'), (9, b'Nine')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='well',
            name='string',
            field=models.IntegerField(default=1, choices=[(1, b'One'), (2, b'Two'), (3, b'Three'), (4, b'Four'), (5, b'Five'), (6, b'Six')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='well',
            name='xmas_tree',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tower',
            name='x_coordinate',
            field=models.IntegerField(verbose_name=b'X Coordinates(UTM)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tower',
            name='y_coordinate',
            field=models.IntegerField(verbose_name=b'Y Coordinates(UTM)'),
            preserve_default=True,
        ),
    ]
