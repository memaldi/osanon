# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151121_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='metadataURL',
            field=models.URLField(default=None),
            preserve_default=False,
        ),
    ]
