# -*- coding: iso-8859-15 -*-

from django.shortcuts import render, redirect
from django.utils.translation import get_language
from django.core.mail import send_mail
from core.models import Center
from core import forms
import googlemaps
import collections
from geopy.distance import vincenty
from scripts import parser
from osanon.settings import GOOGLE_MAPS_KEY
# Create your views here.

def index(request):
    return render(request, 'core/base.html')

def contact(request, center_id):
    center = Center.objects.get(id=center_id)
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        print form
        if form.is_valid():
            send_mail('[OsaNon] Error en el centro #%s' % center_id,
                      form.data['text'], form.data['email'],
                      ['m.emaldi@gmail.com'], fail_silently=False)
            return render(request, 'core/contact_thanks.html')
    else:
        form = forms.ContactForm()
    context = {'form': form, 'center': center}
    return render(request, 'core/contact.html', context)

def results_coordinates(request, lat, lng, offset=1):
    lang = 'es'
    if get_language() in ['es', 'eu']:
        lang = get_language()

    filter_list = []

    centers = []
    if request.method == 'POST':
        for key in request.POST:
            if request.POST[key] == 'on':
                filter_list.append(key)
                centers.extend(Center.objects.filter(language=lang, center_type=key).all())
    else:
        centers = Center.objects.filter(language=lang).all()

    print lat, lng
    destinations = {}
    item_count = 0

    for destination in centers:
        if destination.lat is not None and destination.lng is not None:
            # dist = math.hypot(float(lat) - destination.lat, float(lng) - destination.lng)
            dist = vincenty((float(lat), float(lng)), (destination.lat, destination.lng)).kilometers
            if dist not in destinations.keys():
                destinations[dist] = []
            destinations[dist].append(destination)
            item_count += 1

    ordered_list = []
    ordered_destinations = collections.OrderedDict(sorted(destinations.items()))
    for key in ordered_destinations.keys():
        for item in ordered_destinations[key]:
            ordered_list.append(item)

    destinations_list = []

    limit = 10 * int(offset)
    print limit, (int(offset) - 1) * 10
    for item in ordered_list[(int(offset) - 1) * 10:limit]:
        destinations_list.append((item.lat, item.lng))
        print item.name, key, item.lat, item.lng, item.street

    gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)
    distances = gmaps.distance_matrix([(float(lat), float(lng))], destinations_list, mode='walking')

    distances_dict = []
    for distance, item in zip(distances['rows'][0]['elements'], ordered_list[(int(offset) - 1) * 10:limit]):
        distances_dict.append({'center': item, 'distance': distance})
    pagination_size = item_count / 10
    if item_count % 10 > 0:
        pagination_size += 1
    path = '/results/%s/%s' % (lat, lng)
    context = {'distances': distances_dict, 'origin': (float(lat), float(lng)),
               'pagination': range(1, pagination_size + 1), 'offset': int(offset),
               'path': path, 'filter_list': filter_list}

    return render(request, 'core/results.html', context)

def results_address(request):
    address = request.POST['address']
    lat, lng = parser.getCoordinates(address)
    if None not in [lat, lng]:
        return redirect('/results/%s/%s' % (lat, lng))
    else:
        return render(request, 'core/not_found.html', {'address': address})
