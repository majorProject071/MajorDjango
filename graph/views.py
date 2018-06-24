#import necessary headers
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Sum, Max
from django.shortcuts import render
from time import sleep
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.db import connections
from geopy.geocoders import Nominatim

from .models import *
import json
from news_extraction.models import *
from news_extraction.modules.location_tree import LocationInformation
import news_extraction.modules.vehicles_gazetter as Vehicles
from django.core import serializers
from django.http import JsonResponse
import requests
import geocoder

def index (request):
    location = rssdata.objects.values_list('location', flat=True)
    data = rssdata.objects.values('location').annotate(total=Sum('death_no'))
    totalno = rssdata.objects.values('date').aggregate(total=Count('date'))
    datas = list(data)
    print (datas)
    latitude = []

    for locations in location:
        if locations is not None:
            if(len(locations)>2):
                loc = locations
                g = geocoder.google(loc)
                if g.lat is not None:
                    locs = (g.lat, g.lng)
                    latitude.append(locs)

                # location = results[0]['geometry']['location']
                # print(location['lat'], location['lng'])

                #
                # geolocator = Nominatim()
                # locations = geolocator.geocode(loc)
                # location = (locations.latitude, locations.longitude)
                # latitude.append(location)
    print(latitude)

    context={
            'personal_detail': json.dumps(datas),
            'data':data,
            'latitude':latitude,
            'totalno': totalno,
    }
    return render(request, "heatmap.html", context)


def districts(request):
    data = []
    locations = rssdata.objects.values('location').order_by('location').annotate(value=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('death_no'))
    # print locations
    ktm_location = LocationInformation().all_ktm_locations()
    bkt_location = LocationInformation().all_bkt_locations()
    ltp_location = LocationInformation().all_ltp_locations()
    outside_location = LocationInformation().all_locations()
    ktm_death = 0
    ltp_death = 0
    bkt_death = 0
    for location in locations:
        if location['location'] in ktm_location:
            ktm_death += location['value']
            data.append({'location':'Kathmandu', 'value':ktm_death, 'count':location['count']})
        elif location['location'] in ltp_location:
            ltp_death += location['value']
            data.append({'location': 'Kathmandu', 'value': ltp_death, 'count':location['count']})
        elif location['location'] in bkt_location:
            bkt_death += location['value']
            data.append({'location': 'Kathmandu', 'value': bkt_death, 'count':location['count']})
        elif location['location'] in outside_location:
            data.append({'location':location['location'].capitalize(), 'value': location['value'], 'injury':location['injury'],'count':location['count']})
        else:
            pass

    print ("data : " + str(data))

    context = {
        'newdata': json.dumps(data),
    }
    return render(request, "districts.html", context)

def check(request):
    newdata = rssdata.objects.values('location').annotate(value=Sum('death_no')).order_by('-id')
    data = list(newdata)
    print(data)
    return render(request, "check.html")

def location(request):
    if request.POST:
        vehicleinfo = request.POST.get('vehicle', None)
        if vehicleinfo == '1':
            vehicles = ['Bus', 'Car', 'Truck', 'Tripper', 'Bike', 'Jeep', 'Zeep', 'Scooter', 'Scooty',
                        'Motorbike', 'Motorcycle', 'Container', 'SUV', 'Tractor', 'Moped', 'Lorry',
                        'Minivan', 'Minibus', 'Trolley', 'Tempo']
            vehicledata = []
            vehicle = []
            totalno = rssdata.objects.values('location').aggregate(total=Count('location'))
            newdata = rssdata.objects.values('location', 'vehicle_involved').order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no'))
            for data in newdata:
                if len(data['location']) > 2:
                    vehicle.append({'location': data['location'].capitalize(), 'death': data['death'],'injury': data['injury']})
                    for v in vehicles:
                        if v in data['vehicle_involved']:
                            if v in vehicledata:
                                pass
                            else:
                                vehicledata.append(v)
            context = {
                'location_data': json.dumps(vehicle),
                'totalno': totalno,
                'vehiclelist': vehicledata,
            }
            return render(request, "location.html", context)
        else:
            vehicles = ['Bus', 'Car', 'Truck', 'Tripper', 'Bike', 'Jeep', 'Zeep', 'Scooter', 'Scooty',
                        'Motorbike', 'Motorcycle', 'Container', 'SUV', 'Tractor', 'Moped', 'Lorry',
                        'Minivan', 'Minibus', 'Trolley', 'Tempo']
            vehicledata = []
            vehicle =[]
            totalno = rssdata.objects.values('location').aggregate(total=Count('location'))
            newdata = rssdata.objects.values('location','vehicle_involved').order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no'))
            for data in newdata:
                if len(data['location']) > 2:
                    if vehicleinfo in data['vehicle_involved']:
                        vehicle.append({'location': data['location'].capitalize(), 'death': data['death'],'injury': data['injury']})
                    for v in vehicles:
                        if v in data['vehicle_involved']:
                            if v in vehicledata:
                                pass
                            else:
                                vehicledata.append(v)
            print vehicle



            context = {
                'location_data': json.dumps(vehicle),
                'totalno': totalno,
                'vehiclelist': vehicledata,
            }
            return render(request, "location.html", context)
    vehicles = ['Bus', 'Car', 'Truck', 'Tripper', 'Bike', 'Jeep', 'Zeep', 'Scooter', 'Scooty',
                        'Motorbike', 'Motorcycle', 'Container', 'SUV', 'Tractor', 'Moped', 'Lorry',
                        'Minivan', 'Minibus', 'Trolley', 'Tempo']
    vehicledata = []
    vehicle = []
    totalno = rssdata.objects.values('location').aggregate(total=Count('location'))
    newdata = rssdata.objects.values('location', 'vehicle_involved').order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no'))
    for data in newdata:
        if len(data['location']) > 2:
            vehicle.append({'location': data['location'].capitalize(), 'death': data['death'], 'injury': data['injury']})
            for v in vehicles:
                if v in data['vehicle_involved']:
                    if v in vehicledata:
                        pass
                    else:
                        vehicledata.append(v)
    print vehicle

    context = {
        'location_data': json.dumps(vehicle),
        'totalno': totalno,
        'vehiclelist': vehicledata,
    }
    return render(request, "location.html", context)

def locationdetail(request):
    if request.POST:
        vehicleinfo = request.POST.get('vehicle', None)
        print vehicleinfo
        if vehicleinfo == '1':
            vehicles = ['bus', 'car', 'truck', 'tripper', 'bike', 'jeep', 'zeep', 'scooter', 'scooty',
                        'motorbike', 'motorcycle', 'container', 'SUV', 'tractor', 'moped', 'lorry',
                        'minivan', 'minibus', 'trolley', 'tempo']
            vehicledata = []
            newdata = rssdata.objects.values('location').order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no'))
            totalno = rssdata.objects.values('location').aggregate(total=Count('location'))
            vehiclelist = rssdata.objects.values('vehicle_involved').order_by('vehicle_involved').annotate(total=Count('vehicle_involved'))
            for vehicle in vehiclelist:
                for v in vehicles:
                    if v in vehicle['vehicle_involved']:
                        print v
                        if v in vehicledata:
                            print("data already there.")
                        else:
                            vehicledata.append(v)
            print vehicledata
            data = []
            for nd in newdata:
                if nd['location'] is not None:
                    if len(nd['location']) > 2:
                        data.append(nd)
            context = {
                'location_data': json.dumps(data),
                'totalno': totalno,
                'vehiclelist': vehicledata,
            }
            return render(request, "location.html", context)
        else:
            vehicles = ['Bus', 'Car', 'Truck', 'Bike']
            vehicledata = []
            vehicle =[]
            newdata = rssdata.objects.values('location','vehicle_involved').order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no'))
            for data in newdata:
                if len(data['location']) > 2:
                    if vehicleinfo in data['vehicle_involved']:
                        vehicle.append({'location': data['location'].capitalize(), 'death': data['death'],'injury': data['injury']})
            print vehicle
            vehiclelist = rssdata.objects.values('vehicle_involved').order_by('vehicle_involved').annotate(total=Count('vehicle_involved'))
            for listvehicle in vehiclelist:
                for v in vehicles:
                    if v in listvehicle['vehicle_involved']:
                        if v in vehicledata:
                            print("data already there.")
                        else:
                            vehicledata.append(v)

            context = {
                'vehicleinfo': json.dumps(vehicle),
                'vehiclelist': vehicledata,
            }
            return render(request, "locationdetail.html", context)

def bar (request):
    newdata = rssdata.objects.values('location').annotate( total=Sum('death_no')).order_by('-id')
    alldata = rssdata.objects.values('year').order_by('year').annotate( total=Count('year'))
    alllocation = News.objects.values('Location').order_by('Location').annotate( total=Count('Location'))
    maxvalue = News.objects.values('Location').annotate( total=Sum('Death')).aggregate( maxvalue = Max('total'))
    totalno = News.objects.values('Year').aggregate( total=Count('Year'))
    data = list(newdata)
    print(data)
    context={
            'personal_detail': json.dumps(data),
            'alldata' : alldata,
            'alllocation' : alllocation,
            'maxvalue' : maxvalue,
            'totalno' : totalno,
            'newdata':newdata,
    }
    return render(request, "bar.html", context)

def yeargraph(request, id=None):
    newdata = News.objects.values('Location').annotate( total=Sum('Death')).filter(Year=id).order_by('-id')
    alldata = News.objects.values('Year').order_by('Year').annotate( total=Count('Year'))
    alllocation = News.objects.values('Location').order_by('Location').annotate( total=Count('Location'))
    maxvalue = News.objects.values('Location').annotate( total=Sum('Death')).aggregate( maxvalue = Max('total'))
    totalno = News.objects.values('Year').aggregate( total=Count('Year'))
    data = list(newdata)
    print(data)

    context={
            'personal_detail': json.dumps(data),
            'alldata' : alldata,
            'alllocation' : alllocation,
            'maxvalue' : maxvalue,
            'totalno' : totalno,
            'newdata':newdata,
    }
    return render (request, "baryear.html", context)

def line(request):
    newdata = News.objects.values('Location').annotate( total=Sum('Death')).order_by('-id')
    alldata = News.objects.values('Year').order_by('Year').annotate( total=Count('Year'))
    alllocation = News.objects.values('Location').order_by('Location').annotate( total=Count('Location'))
    maxvalue = News.objects.values('Location').annotate( total=Sum('Death')).aggregate( maxvalue = Max('total'))
    totalno = News.objects.values('Year').aggregate( total=Count('Year'))
    data = list(newdata)
    print(data)
    context={
            'personal_detail': json.dumps(data),
            'alldata' : alldata,
            'alllocation' : alllocation,
            'maxvalue' : maxvalue,
            'totalno' : totalno,
            'newdata':newdata,
    }
    return render (request, "linegraph.html",context)
