# import necessary headers
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Sum, Max, Value
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

def locationcheck(locationlist):
    ktm_location = LocationInformation().all_ktm_locations()
    bkt_location = LocationInformation().all_bkt_locations()
    ltp_location = LocationInformation().all_ltp_locations()
    outside_location = LocationInformation().all_locations()
    ktm_death = 0
    ktm_count = 0
    ktm_injury = 0
    ltp_death = 0
    ltp_count = 0
    ltp_injury = 0
    bkt_death = 0
    bkt_count = 0
    bkt_injury = 0
    maplocations = []
    locations = []
    for location in locationlist:
        if len(location['location']) > 2:
            locations.append(
                {'location': location['location'].capitalize(), 'death': location['death'],
                 'injury': location['injury']})
            if location['location'] in ktm_location:
                ktm_death += location['death']
                ktm_injury += location['injury']
                ktm_count += location['count']
                maplocations.append({'location': 'Kathmandu', 'injury': ktm_injury, 'value': ktm_death, 'count': ktm_count})
            elif location['location'] in ltp_location:
                ltp_death += location['death']
                ltp_injury += location['injury']
                ltp_count += location['count']
                maplocations.append({'location': 'Lalitpur', 'injury': ltp_injury, 'value': ltp_death, 'count': ltp_count})
            elif location['location'] in bkt_location:
                bkt_death += location['death']
                bkt_injury += location['injury']
                bkt_count += location['count']
                maplocations.append({'location': 'Bhaktapur', 'injury': bkt_injury, 'value': bkt_death, 'count': bkt_count})
            elif location['location'] in outside_location:
                maplocations.append({'location': location['location'].capitalize(), 'value': location['death'],
                             'injury': location['injury'], 'count': location['count']})
            else:
                pass
    return (locations ,maplocations)

def index(request):
    location = rssdata.objects.values_list('location', flat=True)
    data = rssdata.objects.values('location').annotate(total=Sum('death_no'))
    totalno = rssdata.objects.values('date').aggregate(total=Count('date'))
    datas = list(data)
    print (datas)
    latitude = []

    for locations in location:
        if locations is not None:
            if (len(locations) > 2):
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

    context = {
        'personal_detail': json.dumps(datas),
        'data': data,
        'latitude': latitude,
        'totalno': totalno,
    }
    return render(request, "heatmap.html", context)


def districts(request):
    data = []
    locations = rssdata.objects.values('location').order_by('location').annotate(value=Sum('death_no')).annotate(
        injury=Sum('injury_no')).annotate(count=Count('death_no'))
    # print locations
    ktm_location = LocationInformation().all_ktm_locations()
    bkt_location = LocationInformation().all_bkt_locations()
    ltp_location = LocationInformation().all_ltp_locations()
    outside_location = LocationInformation().all_locations()
    ktm_death= 0
    ktm_count=0
    ktm_injury = 0
    ltp_death=0
    ltp_count = 0
    ltp_injury = 0
    bkt_death= 0
    bkt_count = 0
    bkt_injury = 0
    for location in locations:
        print location['location']
        if location['location'] in ktm_location:
            ktm_death += location['value']
            ktm_injury += location['injury']
            ktm_count += location['count']
            data.append({'location': 'Kathmandu', 'injury': ktm_injury, 'value': ktm_death, 'count': ktm_count})
        elif location['location'] in ltp_location:
            ltp_death += location['value']
            ltp_injury += location['injury']
            ltp_count += location['count']
            data.append({'location': 'Lalitpur', 'injury': ltp_injury, 'value': ltp_death, 'count': ltp_count})
        elif location['location'] in bkt_location:
            bkt_death += location['value']
            bkt_injury += location['injury']
            bkt_count += location['count']
            data.append({'location': 'Bhaktapur', 'injury': bkt_injury, 'value': bkt_death, 'count': bkt_count})
        elif location['location'] in outside_location:
            data.append({'location': location['location'].capitalize(), 'value': location['value'],
                         'injury': location['injury'], 'count': location['count']})
        else:
            pass


    context = {
        'newdata': json.dumps(data),
    }
    return render(request, "districts.html", context)


def check(request):
    locationlist = rssdata.objects.values('location').annotate(value=Sum('death_no')).order_by('-id')
    data = list(locationlist)
    print(data)
    return render(request, "check.html")


def location(request):
    yearlist = rssdata.objects.values('year').order_by('year').annotate(count=Count('year'))
    locationlist = rssdata.objects.values('location').order_by('location').annotate(
        count=Count('location')).annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no'))
    vehiclelist = rssdata.objects.values('vehicleone').order_by('vehicleone').annotate(count=Count('vehicleone'))
    vehiclelisttwo = rssdata.objects.values('vehicletwo').order_by('vehicletwo').annotate(count=Count('vehicletwo'))
    seasonlist = rssdata.objects.values('season').order_by('season').annotate(count=Count('season'))
    totalno = rssdata.objects.values('location').aggregate(total=Count('location'))
    vehicledata = []
    # assigning vehicle for select tag
    for data in vehiclelist:
        if len(data['vehicleone']) > 2:
            vehicledata.append(data['vehicleone'])
    for newdata in vehiclelisttwo:
        if len(newdata['vehicletwo'])>2:
            if newdata['vehicletwo'] in vehicledata:
                pass
            else:
                vehicledata.append(newdata['vehicletwo'])

    if request.POST:
        vehicleinfo = request.POST.get('vehicle', None)
        yearinfo = request.POST.get('year', None)
        seasoninfo = request.POST.get('season', None)

        if vehicleinfo == '1' and yearinfo == '1' and seasoninfo == '1':
            locations,maplocations = locationcheck(locationlist)

            context = {
                'location_data': json.dumps(locations),
                'totalno': totalno,
                'vehiclelist': vehicledata,
                'yearlist': yearlist,
                'seasonlist': seasonlist,
                'newdata': json.dumps(maplocations),
            }
            return render(request, "location.html", context)

        elif vehicleinfo != '1' and yearinfo == '1' and seasoninfo =='1':
            locationdataone = rssdata.objects.values('location').filter(vehicleone=vehicleinfo).order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))
            locationdatatwo = rssdata.objects.values('location').filter(vehicletwo=vehicleinfo).order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))

            locationdata = list(locationdataone | locationdatatwo)

            locations,maplocations = locationcheck(locationdata)
            info = "by " + vehicleinfo
            context = {
                'location_data': json.dumps(locations),
                'totalno': totalno,
                'vehiclelist': vehicledata,
                'yearlist': yearlist,
                'seasonlist': seasonlist,
                'newdata': json.dumps(maplocations),
                'info': info,
            }


            return render(request, "location.html", context)

        elif vehicleinfo == '1' and yearinfo != '1' and seasoninfo == '1':
            locationdata = list(rssdata.objects.values('location').filter(year=yearinfo).annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location')))

            locations,maplocations = locationcheck(locationdata)
            info = "in " + yearinfo
            context = {
                'location_data': json.dumps(locations),
                'totalno': totalno,
                'vehiclelist': vehicledata,
                'yearlist': yearlist,
                'seasonlist': seasonlist,
                'newdata': json.dumps(maplocations),
                'info': info,
            }

            return render(request, "location.html", context)

        elif vehicleinfo == '1' and yearinfo == '1' and seasoninfo != '1':
            locationdata = list(rssdata.objects.values('location').filter(season=seasoninfo).annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location')))

            locations,maplocations = locationcheck(locationdata)

            info = "during " + seasoninfo

            context = {
                'location_data': json.dumps(locations),
                'totalno': totalno,
                'vehiclelist': vehicledata,
                'yearlist': yearlist,
                'seasonlist': seasonlist,
                'newdata': json.dumps(maplocations),
                'info': info,
            }
            return render(request, "location.html", context)

        elif vehicleinfo != '1' and yearinfo != '1' and seasoninfo == '1':
            locationdataone = rssdata.objects.values('location').filter(vehicleone=vehicleinfo).filter(year=yearinfo).order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))
            locationdatatwo = rssdata.objects.values('location').filter(vehicletwo=vehicleinfo).filter(year=yearinfo).order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))

            locationdata = list(locationdataone | locationdatatwo)

            locations, maplocations = locationcheck(locationdata)


            info = "by " + vehicleinfo + " in " + yearinfo

            context = {
                'location_data': json.dumps(locations),
                'totalno': totalno,
                'vehiclelist': vehicledata,
                'yearlist': yearlist,
                'seasonlist': seasonlist,
                'info': info,
                'newdata': json.dumps(maplocations),
            }

            return render(request, "location.html", context)

        elif vehicleinfo != '1' and yearinfo == '1' and seasoninfo != '1':
            locationdataone = rssdata.objects.values('location').filter(vehicleone=vehicleinfo).filter(season=seasoninfo).order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))
            locationdatatwo = rssdata.objects.values('location').filter(vehicletwo=vehicleinfo).filter(season=seasoninfo).order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))

            locationdata = list(locationdataone | locationdatatwo)

            locations, maplocations = locationcheck(locationdata)

            info = "by " + vehicleinfo + " during " + seasoninfo

            context = {
                'location_data': json.dumps(locations),
                'totalno': totalno,
                'vehiclelist': vehicledata,
                'yearlist': yearlist,
                'seasonlist': seasonlist,
                'info': info,
                'newdata': json.dumps(maplocations),
            }

            return render(request, "location.html", context)

        elif vehicleinfo == '1' and yearinfo != '1' and seasoninfo != '1':
            locationdata = list(rssdata.objects.values('location').filter(season=seasoninfo).filter(year=yearinfo).annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location')))

            locations, maplocations = locationcheck(locationdata)

            info = "in " + yearinfo + " during " + seasoninfo

            context = {
                'location_data': json.dumps(locations),
                'totalno': totalno,
                'vehiclelist': vehicledata,
                'yearlist': yearlist,
                'seasonlist': seasonlist,
                'info': info,
                'newdata': json.dumps(maplocations)
            }
            return render(request, "location.html", context)

        elif vehicleinfo != '1' and yearinfo != '1' and seasoninfo != '1':
            locationdataone = rssdata.objects.values('location').filter(vehicleone=vehicleinfo).filter(season=seasoninfo).filter(year=yearinfo).order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))
            locationdatatwo = rssdata.objects.values('location').filter(vehicletwo=vehicleinfo).filter(season=seasoninfo).filter(year=yearinfo).order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))

            locationdata = list(locationdataone | locationdatatwo)

            locations, maplocations = locationcheck(locationdata)

            info = "by " + vehicleinfo + " in " + yearinfo + " during " + seasoninfo

            context = {
                'location_data': json.dumps(locations),
                'totalno': totalno,
                'vehiclelist': vehicledata,
                'yearlist': yearlist,
                'seasonlist': seasonlist,
                'info' : info,
                'newdata': json.dumps(maplocations),
            }

            return render(request, "location.html", context)


    locations, maplocations = locationcheck(locationlist)
    context = {
        'location_data': json.dumps(locations),
        'totalno': totalno,
        'vehiclelist': vehicledata,
        'yearlist': yearlist,
        'seasonlist': seasonlist,
        'newdata': json.dumps(maplocations),
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
            locationlist = rssdata.objects.values('location').order_by('location').annotate(
                death=Sum('death_no')).annotate(injury=Sum('injury_no'))
            totalno = rssdata.objects.values('location').aggregate(total=Count('location'))
            vehiclelist = rssdata.objects.values('vehicleone').order_by('vehicleone').annotate(
                total=Count('vehicleone'))
            for vehicle in vehiclelist:
                for v in vehicles:
                    if v in vehicle['vehicleone']:
                        print v
                        if v in vehicledata:
                            print("data already there.")
                        else:
                            vehicledata.append(v)
            print vehicledata
            data = []
            for nd in locationlist:
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
            vehicle = []
            locationlist = rssdata.objects.values('location', 'vehicleone').order_by('location').annotate(
                death=Sum('death_no')).annotate(injury=Sum('injury_no'))
            for data in locationlist:
                if len(data['location']) > 2:
                    if vehicleinfo in data['vehicleone']:
                        vehicle.append({'location': data['location'].capitalize(), 'death': data['death'],
                                        'injury': data['injury']})
            print vehicle
            vehiclelist = rssdata.objects.values('vehicleone').order_by('vehicleone').annotate(
                total=Count('vehicleone'))
            for listvehicle in vehiclelist:
                for v in vehicles:
                    if v in listvehicle['vehicleone']:
                        if v in vehicledata:
                            print("data already there.")
                        else:
                            vehicledata.append(v)

            context = {
                'vehicleinfo': json.dumps(vehicle),
                'vehiclelist': vehicledata,
            }
            return render(request, "locationdetail.html", context)


def bar(request):
    locationlist = rssdata.objects.values('location').annotate(total=Sum('death_no')).order_by('-id')
    alldata = rssdata.objects.values('year').order_by('year').annotate(total=Count('year'))
    alllocation = News.objects.values('Location').order_by('Location').annotate(total=Count('Location'))
    maxvalue = News.objects.values('Location').annotate(total=Sum('Death')).aggregate(maxvalue=Max('total'))
    totalno = News.objects.values('Year').aggregate(total=Count('Year'))
    data = list(locationlist)
    print(data)
    context = {
        'personal_detail': json.dumps(data),
        'alldata': alldata,
        'alllocation': alllocation,
        'maxvalue': maxvalue,
        'totalno': totalno,
        'locationlist': locationlist,
    }
    return render(request, "bar.html", context)


def yeargraph(request, id=None):
    locationlist = News.objects.values('Location').annotate(total=Sum('Death')).filter(Year=id).order_by('-id')
    alldata = News.objects.values('Year').order_by('Year').annotate(total=Count('Year'))
    alllocation = News.objects.values('Location').order_by('Location').annotate(total=Count('Location'))
    maxvalue = News.objects.values('Location').annotate(total=Sum('Death')).aggregate(maxvalue=Max('total'))
    totalno = News.objects.values('Year').aggregate(total=Count('Year'))
    data = list(locationlist)
    print(data)

    context = {
        'personal_detail': json.dumps(data),
        'alldata': alldata,
        'alllocation': alllocation,
        'maxvalue': maxvalue,
        'totalno': totalno,
        'locationlist': locationlist,
    }
    return render(request, "baryear.html", context)


def line(request):
    locationlist = News.objects.values('Location').annotate(total=Sum('Death')).order_by('-id')
    alldata = News.objects.values('Year').order_by('Year').annotate(total=Count('Year'))
    alllocation = News.objects.values('Location').order_by('Location').annotate(total=Count('Location'))
    maxvalue = News.objects.values('Location').annotate(total=Sum('Death')).aggregate(maxvalue=Max('total'))
    totalno = News.objects.values('Year').aggregate(total=Count('Year'))
    data = list(locationlist)
    print(data)
    context = {
        'personal_detail': json.dumps(data),
        'alldata': alldata,
        'alllocation': alllocation,
        'maxvalue': maxvalue,
        'totalno': totalno,
        'locationlist': locationlist,
    }
    return render(request, "linegraph.html", context)
