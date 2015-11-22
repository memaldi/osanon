# coding=utf-8

from django.db import models

# Create your models here.

class Center(models.Model):
    name = models.CharField(max_length=100)
    pc = models.IntegerField(null=True)
    street = models.CharField(max_length=200, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    BIZKAIA = 'BK'
    GIPUZKOA = 'GP'
    ARABA = 'AB'
    PROVINCE_CHOICES = (
        (BIZKAIA, 'Bizkaia'),
        (GIPUZKOA, 'Gipuzkoa'),
        (ARABA, 'Araba')
    )
    province = models.CharField(max_length=20, choices=PROVINCE_CHOICES, default=BIZKAIA)
    town = models.CharField(max_length=30)
    BOTIQUIN = 'BT'
    CENTRO_DE_SALUD = 'CS'
    HOSPITALES = 'HT'
    FARMACIA = 'FM'
    # TYPE_CHOICES = (
    #     (BOTIQUIN, 'Botiquín'),
    #     (CENTRO_DE_SALUD, 'Centro de salud'),
    #     (HOSPITALES, 'Hospital'),
    #     (FARMACIA, 'Farmacia'),
    # )
    center_type = models.CharField(max_length=20)
    SPANISH = 'ES'
    BASQUE = 'EU'
    LANGUAGE_CHOICES = (
        (SPANISH, 'es'),
        (BASQUE, 'eu')
    )
    language = models.CharField(max_length=2, default=SPANISH)
    metadataURL = models.URLField()
