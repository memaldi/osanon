# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_center_metadataurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='town',
            field=models.CharField(max_length=50),
        ),
    ]
