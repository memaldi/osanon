# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151117_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='street',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
