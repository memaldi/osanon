# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='language',
            field=models.CharField(default=b'ES', max_length=2, choices=[(b'ES', b'es'), (b'EU', b'eu')]),
        ),
        migrations.AlterField(
            model_name='center',
            name='_type',
            field=models.CharField(max_length=20, choices=[(b'BT', b'Botiqu\xc3\xadn'), (b'CS', b'Centro de salud'), (b'HT', b'Hospital'), (b'FM', b'Farmacia')]),
        ),
    ]
