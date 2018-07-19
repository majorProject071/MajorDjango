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
import datetime

#provide parameter to select tag for location in location.html
def selectparameters():
    listoflocation = rssdata.objects.values('location').order_by('location').annotate(count=Count('location'))
    ktm_location = LocationInformation().all_ktm_locations()
    bkt_location = LocationInformation().all_bkt_locations()
    ltp_location = LocationInformation().all_ltp_locations()
    outside_location = LocationInformation().all_locations()
    locationlist = []
    ktmlocationlist = []
    ltplocationlist = []
    bktlocationlist = []
    for location in listoflocation:
        if len(location['location']) > 2:
            if location['location'] in ktm_location:
                ktmlocationlist.append({'location':location['location'].capitalize()})
                if (len(locationlist) == 0):
                    locationlist.append('Kathmandu')
                if 'Kathmandu' in locationlist:
                    pass
                else:
                    locationlist.append('Kathmandu')
            elif location['location'] in ltp_location:
                ltplocationlist.append({'location': location['location'].capitalize()})
                if (len(locationlist) == 0):
                    locationlist.append('Lalitpur')
                if 'Lalitpur' in locationlist:
                    pass
                else:
                    locationlist.append('Lalitpur')
            elif location['location'] in bkt_location:
                bktlocationlist.append({'location': location['location'].capitalize()})
                if (len(locationlist) == 0):
                    locationlist.append('Bhaktapur')
                if 'Bhaktapur' in locationlist:
                    pass
                else:
                    locationlist.append('Bhaktapur')
            elif location['location'] in outside_location:
                locationlist.append(location['location'].capitalize())
            else:
                pass
    return (locationlist, ktmlocationlist, ltplocationlist, bktlocationlist)

#provide quieres to location()
def getqueries(informations, ktmlocations, ltplocations, bktlocations):
    newlocationlist = rssdata.objects.all().values('location', 'year', 'month', 'season', 'vehicleone',
                                                   'vehicletwo','date').order_by('location').annotate(count=Count('location')).annotate(
                                                    deathno=Sum('death_no')).annotate(injuryno=Sum('injury_no'))
    information = ''
    distinctlocations = []
    querieslist = []
    countlist = []
    for info in informations:
        if info['locationinfo'] != '1':
            newlocationlist = locationcheck(info['locationinfo'], ktmlocations,ltplocations, bktlocations)
            string = ' at ' + str(info['locationinfo'])
            information = information + string
        if info['ltplocationinfo'] != '1':
            newlocationlist = newlocationlist.filter(location=info['ltplocationinfo'].lower())
            string = ' in ' + info['ltplocationinfo']
            information = information + string
        if info['ktmlocationinfo'] != '1':
            newlocationlist = newlocationlist.filter(location=info['ktmlocationinfo'].lower())
            string = ' in ' + info['ktmlocationinfo']
            information = information + string
        if info['bktlocationinfo'] != '1':
            newlocationlist = newlocationlist.filter(location=info['bktlocationinfo'].lower())
            string = ' in ' + info['bktlocationinfo']
            information = information + string
        if info['yearinfo'] != '1':
            newlocationlist = newlocationlist.filter(year=info['yearinfo'])
            string = ' in ' + str(info['yearinfo'])
            information = information + string
        if info['monthinfo'] != '1':
            if info['monthinfo'] == '5' or info['monthinfo'] == '10':
                value = int(info['monthinfo'])
                timeago = (datetime.date.today() - datetime.timedelta(value * 365 / 12)).isoformat()
                newlocationlist = newlocationlist.filter(date__gte=timeago)
                string =' '  + info['monthinfo'] + ' months ago '
                information = information + string
            else:
                newlocationlist = newlocationlist.filter(month=info['monthinfo'])
                string = ' in ' + info['monthinfo']
                information = information + string
        if info['seasoninfo'] != '1':
            newlocationlist = newlocationlist.filter(season=info['seasoninfo'])
            string = ' in ' + info['seasoninfo']
            information = information + string
        if info['vehicleinfo'] != '1':
            newlocationlist = newlocationlist.filter(vehicleone=info['vehicleinfo']) or newlocationlist.filter(vehicleone=info['vehicleinfo'])
            string = ' by ' + info['vehicleinfo']
            information = information + string
    for samelocation in newlocationlist:
        if len(samelocation['location'])>2:
            if samelocation['location'] in distinctlocations:
                pass
            else:
                distinctlocations.append(samelocation['location'])
        else:
            pass

    for distlocation in distinctlocations:
        newqueries = newlocationlist.filter(location=distlocation)
        death = 0
        injury = 0
        count = 0
        for queries in newqueries:
            death += queries['deathno']
            injury += queries['injuryno']
            count += queries['count']
        querieslist.append({'location': distlocation.capitalize(), 'death': death , 'injury': injury })
        countlist.append({'location': distlocation.capitalize(), 'death': death , 'injury': injury ,'count': count})
    return newlocationlist, querieslist, information, len(querieslist), countlist

def locationcheck(locationinfo, ktmlocationlist,ltplocationlist,bktlocationlist):
    newlocationlist = rssdata.objects.all().values('location', 'year', 'month', 'season', 'vehicleone',
                                                   'vehicletwo', 'date').order_by('location').annotate(
        count=Count('location')).annotate(deathno=Sum('death_no')).annotate(injuryno=Sum('injury_no'))
    locationlist = rssdata.objects.none()
    if locationinfo == 'Kathmandu':
        for z in range(0, len(ktmlocationlist)):
            if(z ==0):
                onelocationlist = newlocationlist.filter(location=ktmlocationlist[0]['location'].lower())
                locationlist = onelocationlist
            if (z>0):
                onelocationlist = newlocationlist.filter(location=ktmlocationlist[z]['location'].lower()) | locationlist
                locationlist = onelocationlist
    elif locationinfo == 'Lalitpur':
        for z in range(0, len(ltplocationlist)):
            if(z ==0):
                onelocationlist = newlocationlist.filter(location=ltplocationlist[0]['location'].lower())
                locationlist = onelocationlist
            if (z>0):
                onelocationlist = newlocationlist.filter(location=ltplocationlist[z]['location'].lower()) | locationlist
                locationlist = onelocationlist
    elif locationinfo == 'Bhaktapur':
        for z in range(0, len(bktlocationlist)):
            if(z ==0):
                onelocationlist = newlocationlist.filter(location=bktlocationlist[0]['location'].lower())
                locationlist = onelocationlist
            if (z>0):
                onelocationlist = newlocationlist.filter(location=bktlocationlist[z]['location'].lower()) | locationlist
                locationlist = onelocationlist
    else:
        onelocationlist = newlocationlist.filter(location=locationinfo.lower())
    return onelocationlist

def finalquery(countlist):
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
    for location in countlist:
        if location['location'].lower() in ktm_location:
            ktm_death += location['death']
            ktm_injury += location['injury']
            ktm_count += location['count']
            maplocations.append({'location': 'Kathmandu', 'injury': ktm_injury, 'value': ktm_death, 'count': ktm_count})
        elif location['location'].lower() in ltp_location:
            ltp_death += location['death']
            ltp_injury += location['injury']
            ltp_count += location['count']
            maplocations.append({'location': 'Lalitpur', 'injury': ltp_injury, 'value': ltp_death, 'count': ltp_count})
        elif location['location'].lower() in bkt_location:
            bkt_death += location['death']
            bkt_injury += location['injury']
            bkt_count += location['count']
            maplocations.append({'location': 'Bhaktapur', 'injury': bkt_injury, 'value': bkt_death, 'count': bkt_count})
        elif location['location'].lower() in outside_location:
            maplocations.append({'location': location['location'].capitalize(), 'value': location['death'],
                             'injury': location['injury'], 'count': location['count']})
        else:
            pass
    return (maplocations)



def location(request):
    listoflocation, ktmlocationlist, ltplocationlist, bktlocationlist = selectparameters()
    yearlist = rssdata.objects.values('year').order_by('year').annotate(count=Count('year'))
    locationlist = rssdata.objects.values('location').order_by('location').annotate(count=Count('location')).annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no'))
    tablelocationlist = rssdata.objects.all().values('location', 'year', 'month', 'season', 'vehicleone',
                                                   'vehicletwo', 'date').order_by('location').annotate(count=Count('location')).annotate(deathno=Sum('death_no')).annotate(injuryno=Sum('injury_no'))
    vehiclelist = rssdata.objects.values('vehicleone').order_by('vehicleone').annotate(count=Count('vehicleone'))
    vehiclelisttwo = rssdata.objects.values('vehicletwo').order_by('vehicletwo').annotate(count=Count('vehicletwo'))
    seasonlist = rssdata.objects.values('season').order_by('season').annotate(count=Count('season'))
    monthlist = rssdata.objects.values('month').order_by('month').annotate(count=Count('month'))
    tablevehiclelist = rssdata.objects.all().values('vehicle_no','location', 'year', 'month', 'season', 'vehicleone',
                                                     'vehicletwo', 'date').order_by('vehicle_no').annotate(
        count=Count('vehicle_no')).annotate(deathno=Sum('death_no')).annotate(injuryno=Sum('injury_no'))

    vehicledata = []
    barlocations = []
    tablelocation = []
    tablevehicle = []
    for loc in tablevehiclelist:
        if len(loc['vehicle_no'])>2:
            if len(loc['location'])>2:
                tablevehicle.append({'location': loc['location'].capitalize(), 'vehicleno': loc['vehicle_no'], 'deathno': loc['deathno'],
                                  'injuryno': loc['injuryno'], 'date': loc['date'], 'year': loc['year'],
                                  'month': loc['month'],
                                  'season': loc['season'], 'vehicleone': loc['vehicleone'],
                                  'vehicletwo': loc['vehicletwo']})
            else:
                tablevehicle.append({'location': 'not defined', 'vehicleno': loc['vehicle_no'],
                                     'deathno': loc['deathno'],
                                     'injuryno': loc['injuryno'], 'date': loc['date'], 'year': loc['year'],
                                     'month': loc['month'],
                                     'season': loc['season'], 'vehicleone': loc['vehicleone'],
                                     'vehicletwo': loc['vehicletwo']})
    for loc in tablelocationlist:
        if len(loc['location']) >2:
            tablelocation.append({'location': loc['location'].capitalize(), 'deathno': loc['deathno'],
                             'injuryno': loc['injuryno'], 'date': loc['date'], 'year': loc['year'], 'month': loc['month'],
                                  'season': loc['season'], 'vehicleone': loc['vehicleone'], 'vehicletwo': loc['vehicletwo']})
    for data in vehiclelist:
        try:
            if len(data['vehicleone']) > 2:
                vehicledata.append(data['vehicleone'])
        except:
            pass
    for newdata in vehiclelisttwo:
        try:
            if len(newdata['vehicletwo'])>2:
                if newdata['vehicletwo'] in vehicledata:
                    pass
                else:
                    vehicledata.append(newdata['vehicletwo'])
        except:
            pass

    valueslist = []
    if request.POST:
        search =  request.POST.get('query', None)
        if search:
            queryset_list = rssdata.objects.filter(vehicle_no__icontains=search).values('location','date','death_no','injury_no','vehicle_no')
            if len(queryset_list) == 0 :
                context = {
                    'locationdetail': tablevehicle,
                    'listoflocation': listoflocation,
                    'ktm_location': ktmlocationlist,
                    'ltp_location': ltplocationlist,
                    'bkt_location': bktlocationlist,
                    'monthlist': monthlist,
                    'vehiclelist': vehicledata,
                    'yearlist': yearlist,
                    'seasonlist': seasonlist,
                }
                return render(request, "findlocation.html", context)
            else:
                print queryset_list
                context = {
                    'location_data': queryset_list,
                    'listoflocation': listoflocation,
                    'ktm_location': ktmlocationlist,
                    'ltp_location': ltplocationlist,
                    'bkt_location': bktlocationlist,
                    'monthlist': monthlist,
                    'vehiclelist': vehicledata,
                    'yearlist': yearlist,
                    'seasonlist': seasonlist,
                    'search' : search,
                }
                return render(request, "findlocation.html", context)



        else:
            valueslist.append({'vehicleinfo': request.POST.get('vehicle', None),
                               'yearinfo': request.POST.get('year', None),
                               'seasoninfo': request.POST.get('season', None),
                               'locationinfo': request.POST.get('location', None),
                               'ktmlocationinfo': request.POST.get('ktmlocation', None),
                               'ltplocationinfo': request.POST.get('ltplocation', None),
                               'bktlocationinfo': request.POST.get('bktlocation', None),
                               'monthinfo': request.POST.get('month', None)})

            newlocationlist, filterlocation, information, totalno, countlist = getqueries(valueslist, ktmlocationlist,
                                                                                          ltplocationlist,
                                                                                          bktlocationlist)

            barlocations = filterlocation
            maplocations = finalquery(countlist)
            if (len(filterlocation) == 0):
                context = {
                    'locationlist': tablelocation,
                    'listoflocation': listoflocation,
                    'ktm_location': ktmlocationlist,
                    'ltp_location': ltplocationlist,
                    'bkt_location': bktlocationlist,
                    'monthlist': monthlist,
                    'vehiclelist': vehicledata,
                    'yearlist': yearlist,
                    'seasonlist': seasonlist,
                }
                return render(request, "findlocation.html", context)

            context = {
                'locationinfos': newlocationlist,
                'location_data': json.dumps(barlocations),
                'listoflocation': listoflocation,
                'ktm_location': ktmlocationlist,
                'ltp_location': ltplocationlist,
                'bkt_location': bktlocationlist,
                'monthlist': monthlist,
                'totalno': totalno,
                'vehiclelist': vehicledata,
                'yearlist': yearlist,
                'seasonlist': seasonlist,
                'info': information,
                'newdata': json.dumps(maplocations),
            }
            return render(request, "location.html", context)


    for locations in locationlist:
        if len(locations['location'])>2:
            barlocations.append({'location': locations['location'].capitalize(), 'death': locations['death'],
                             'injury': locations['injury']})
    totalno = len(locationlist)
    maplocations = finalquery(locationlist)

    context = {
        'locationinfos': tablelocation,
        'location_data': json.dumps(barlocations),
        'listoflocation': listoflocation,
        'ktm_location': ktmlocationlist,
        'ltp_location': ltplocationlist,
        'bkt_location' : bktlocationlist,
        'monthlist' : monthlist,
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
                # print loc
                # g = geocoder.google(loc)
                # print g.lat
                # if g.lat is not None:
                #     locs = (g.lat, g.lng)
                #     latitude.append(locs)
                #
                # location = results[0]['geometry']['location']
                # print(location['lat'], location['lng'])


                geolocator = Nominatim()
                locations = geolocator.geocode(loc)
                location = (locations.latitude, locations.longitude)
                latitude.append(location)
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
