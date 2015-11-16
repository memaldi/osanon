# coding=utf-8

from core.models import Center
from xml.dom.minidom import parseString
from osanon.settings import GOOGLE_MAPS_KEY
import requests
import codecs
import json

CENTROS_DE_SALUD_URL = 'http://opendata.euskadi.eus/contenidos/ds_localizaciones/centros_salud_en_euskadi/opendata/centros-salud.xml'

API_KEY = GOOGLE_MAPS_KEY
GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

def getText(item):
    for node in item:
        for child in node.childNodes:
            if child.nodeType == child.TEXT_NODE:
                return child.data

def getCoordinates(address, town=None):
    r = requests.get(GOOGLE_MAPS_URL, params={'address': address.replace(' ', '+'), 'key': API_KEY, 'language': 'es'})
    json_result = r.json()
    if 'results' in json_result:
        for result in json_result['results']:
            for component in result['address_components']:
                if town is not None:
                    if 'locality' in component['types'] and town in component['short_name']:
                        lat = result['geometry']['location']['lat']
                        lng = result['geometry']['location']['lng']
                        return lat, lng
                if 'administrative_area_level_1' in component['types'] and 'PV' in component['short_name']:
                    lat = result['geometry']['location']['lat']
                    lng = result['geometry']['location']['lng']
                    return lat, lng
    if town is not None:
        r = requests.get(GOOGLE_MAPS_URL, params={'address': address.replace(' ', '+') + '+%s' % town, 'key': API_KEY, 'language': 'es'})
        json_result = r.json()
        if 'results' in json_result:
            for result in json_result['results']:
                for component in result['address_components']:
                    if town is not None:
                        if 'locality' in component['types'] and town in component['short_name']:
                            lat = result['geometry']['location']['lat']
                            lng = result['geometry']['location']['lng']
                            return lat, lng
                    if 'administrative_area_level_1' in component['types'] and 'PV' in component['short_name']:
                        lat = result['geometry']['location']['lat']
                        lng = result['geometry']['location']['lng']
                        return lat, lng

    return None, None

def loadDB():
    r = requests.get(CENTROS_DE_SALUD_URL)
    dom = parseString(codecs.encode(r.text, 'utf-8'))
    for item in dom.getElementsByTagName('row'):
        center = Center()
        center.name = getText(item.getElementsByTagName('sanidadname'))
        address = getText(item.getElementsByTagName('sanidadstreet'))
        center.street = address

        town = getText(item.getElementsByTagName('sanidadtown'))
        center.town = town

        center.lat, center.lng = getCoordinates(address, town=town)
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

        center.center_type = getText(item.getElementsByTagName('sanidadcentertype'))
        center.language = Center.SPANISH

        center.save()
