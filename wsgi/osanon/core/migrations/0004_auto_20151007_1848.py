# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151006_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='center',
            name='lng',
            field=models.FloatField(null=True),
        ),
    ]
