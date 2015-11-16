# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20151007_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='center',
            name='_type',
        ),
        migrations.AddField(
            model_name='center',
            name='center_type',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
    ]
