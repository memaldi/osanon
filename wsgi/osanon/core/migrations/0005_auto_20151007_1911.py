# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151007_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='pc',
            field=models.IntegerField(null=True),
        ),
    ]
