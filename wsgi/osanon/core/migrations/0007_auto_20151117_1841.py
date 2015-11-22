# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151109_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='language',
            field=models.CharField(default=b'ES', max_length=2),
        ),
    ]
