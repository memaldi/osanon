# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151004_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='lat',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='center',
            name='lng',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='center',
            name='street',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='center',
            name='province',
            field=models.CharField(default=b'BK', max_length=20, choices=[(b'BK', b'Bizkaia'), (b'GP', b'Gipuzkoa'), (b'AB', b'Araba')]),
        ),
    ]
