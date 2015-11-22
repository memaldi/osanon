# coding=utf-8

from core.models import Center
from xml.dom.minidom import parseString
from osanon.settings import GOOGLE_MAPS_KEY
import requests
import codecs
import json

URL_DICT = { 'es': {
                    #  'Farmacias': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/farmacias_de_euskadi/opendata/farmacias.xml',
                     'Hospitales': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/hospitales_en_euskadi/opendata/hospitales.xml',
                     'Centros de salud': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/centros_salud_en_euskadi/opendata/centros-salud.xml',
                     'Botiquines': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/botiquines_en_euskadi/opendata/botiquines.xml',
                     'Centros comarcales': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/centros_comarcales_en_euskadi/opendata/comarcas.xml'
             },
             'eu': {
                    # 'Farmaziak': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/farmacias_de_euskadi/opendata/farmaziak.xml',
                    'Ospitaleak': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/hospitales_en_euskadi/opendata/ospitaleak.xml',
                    'Osasun zentroak': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/centros_salud_en_euskadi/opendata/osasun-zentroak.xml',
                    'Botikinak': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/botiquines_en_euskadi/opendata/botikinak.xml',
                    'Eskualde zentroak': 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/centros_comarcales_en_euskadi/opendata/eskualdeak.xml'
             }
}

API_KEY = GOOGLE_MAPS_KEY
GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

def getText(item):
    for node in item:
        for child in node.childNodes:
            if child.nodeType == child.TEXT_NODE:
                return child.data

def getCoordinates(address, town=None):
    if town is not None:
        r = requests.get(GOOGLE_MAPS_URL, params={'address': address.replace(' ', '+') + '+%s' % town, 'key': API_KEY, 'language': 'es'})
        json_result = r.json()
        if 'results' in json_result:
            for result in json_result['results']:
                for component in result['address_components']:
                    if 'locality' in component['types'] and town in component['short_name']:
                        lat = result['geometry']['location']['lat']
                        lng = result['geometry']['location']['lng']
                        print address.replace(' ', '+') + '+%s' % town, lat, lng
                        return lat, lng
                    elif 'administrative_area_level_1' in component['types'] and 'PV' in component['short_name']:
                        lat = result['geometry']['location']['lat']
                        lng = result['geometry']['location']['lng']
                        print address.replace(' ', '+') + '+%s' % town, lat, lng
                        return lat, lng

    r = requests.get(GOOGLE_MAPS_URL, params={'address': address.replace(' ', '+'), 'key': API_KEY, 'language': 'es'})
    json_result = r.json()
    if 'results' in json_result:
        for result in json_result['results']:
            for component in result['address_components']:
                if 'administrative_area_level_1' in component['types'] and 'PV' in component['short_name']:
                    lat = result['geometry']['location']['lat']
                    lng = result['geometry']['location']['lng']
                    return lat, lng

    return None, None

def loadDB():
    for lang in URL_DICT:
        for item_type in URL_DICT[lang]:
            print 'Importing %s (%s)...' % (item_type, lang)
            r = requests.get(URL_DICT[lang][item_type])
            dom = parseString(codecs.encode(r.text, 'utf-8'))
            for item in dom.getElementsByTagName('row'):
                center = Center()
                center.metadataURL = getText(item.getElementsByTagName('metadataxml'))

                existing_center = Center.objects.filter(metadataURL=center.metadataURL).first()
                lat, lng = None, None
                if existing_center is not None:
                    center.lat = existing_center.lat
                    center.lng = existing_center.lng

                center.name = getText(item.getElementsByTagName('sanidadname'))
                address = getText(item.getElementsByTagName('sanidadstreet'))
                center.street = address

                town = getText(item.getElementsByTagName('sanidadtown'))
                center.town = town
                if address is not None and None in [center.lat, center.lng]:
                    center.lat, center.lng = getCoordinates(address, town=town)
                    if existing_center is not None:
                        if None not in [center.lat, center.lng]:
                            existing_center.lat = center.lat
                            existing_center.lng = center.lng
                            existing_center.save()

                try:
                    center.pc = int(getText(item.getElementsByTagName('sanidadpostalcode')))
                except:
                    center.pc = None
                province = getText(item.getElementsByTagName('sanidadprovince'))
                if province == 'ALAVA':
                    center.province = Center.ARABA
                elif province == 'GIPUZKOA':
                    center.province = Center.GIPUZKOA
                elif province == 'Bizkaia':
                    center.province = Center.BIZKAIA

                # center.center_type = getText(item.getElementsByTagName('sanidadcentertype'))
                center.center_type = item_type
                center.language = lang
                try:
                    center.save()
                except:
                    print 'Can not save %s' % center.name
