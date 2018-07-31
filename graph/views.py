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
import nltk
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
import re

# provide parameter to select tag for location in location.html

def selectparameters():
    listoflocation = rssdata.objects.values('location').order_by('location').annotate(count=Count('location'))
    print listoflocation

    # import all location from kathmandu, bhaktapur, lalitpur and outside from location_tree.py
    ktm_location = LocationInformation().all_ktm_locations()
    bkt_location = LocationInformation().all_bkt_locations()
    ltp_location = LocationInformation().all_ltp_locations()
    outside_location = LocationInformation().all_locations()

    # list initialization
    locationlist = []
    ktmlocationlist = []
    ltplocationlist = []
    bktlocationlist = []

    for location in listoflocation:
        # check if location is not []
        if len(location['location']) > 2:
            if location['location'] in ktm_location or location['location'] == "kathmandu":

                #add location under kathmandu
                ktmlocationlist.append({'location':location['location'].capitalize()})
                if (len(locationlist) == 0):
                    locationlist.append('Kathmandu')

                #check repetition of word kathmandu
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
    print informations
    newlocationlist = rssdata.objects.all().values('location', 'year', 'month', 'vehicleone',
                                                   'vehicletwo','date','vehicle_type').order_by('location').annotate(count=Count('location')).annotate(
                                                    deathno=Sum('death_no')).annotate(injuryno=Sum('injury_no'))

    # initialization
    information = ''
    distinctlocations = []
    querieslist = []
    countlist = []

    for info in informations:

        #check for request of user and use flter accordingly

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
            newlocationlist = newlocationlist.filter(month=info['monthinfo'])
            string = ' in ' + info['monthinfo']
            information = information + string

        if info['vehicletypeinfo'] != '1':
            newlocationlist = newlocationlist.filter(vehicle_type__icontains=info['vehicletypeinfo'])
            string = ' by ' + info['vehicletypeinfo']
            information = information + string

        if info['vehicletwoinfo'] != '1':
            newlocationlist = newlocationlist.filter(vehicleone=info['vehicletwoinfo']) or newlocationlist.filter(
                vehicleone=info['vehicletwoinfo'])
            string = ' by ' + info['vehicletwoinfo']
            information = information + string
        if info['vehiclethreeinfo'] != '1':
            newlocationlist = newlocationlist.filter(vehicleone=info['vehiclethreeinfo']) or newlocationlist.filter(
                vehicleone=info['vehiclethreeinfo'])
            string = ' by ' + info['vehiclethreeinfo']
            information = information + string
        if info['vehiclefourinfo'] != '1':
            newlocationlist = newlocationlist.filter(vehicleone=info['vehiclefourinfo']) or newlocationlist.filter(
                vehicleone=info['vehiclefourinfo'])
            string = ' by ' + info['vehiclefourinfo']
            information = information + string

        if info['dateto'] != '1':
            newlocationlist = newlocationlist.filter(date__range=(info['datefrom'], info['dateto']))
            # string = ' from ' + info['datefrom']+ ' to ' + info['dateto']
            # information = information + string
     #extract distinct locations from query
    for samelocation in newlocationlist:
        if len(samelocation['location'])>2:
            if samelocation['location'] in distinctlocations:
                pass
            else:
                distinctlocations.append(samelocation['location'])
        else:
            pass

    #use distince locations to sum up their death and injury number
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

    # return to location()
    return newlocationlist, querieslist, information, len(querieslist), countlist

#return filtered location to getqueries in info location info

def locationcheck(locationinfo, ktmlocationlist,ltplocationlist,bktlocationlist):
    newlocationlist = rssdata.objects.all().values('location', 'year', 'month', 'vehicleone',
                                                   'vehicletwo', 'date').order_by('location').annotate(
        count=Count('location')).annotate(deathno=Sum('death_no')).annotate(injuryno=Sum('injury_no'))

    print locationinfo

    #initialize query
    locationlist = rssdata.objects.none()

    if locationinfo == 'Kathmandu':
        onelocationlist = newlocationlist.filter(location="kathmandu")
        locationlist = onelocationlist
        for z in range(0, len(ktmlocationlist)):
            if(len(locationlist) == 0):
                onelocationlist = newlocationlist.filter(location=ktmlocationlist[0]['location'].lower())
                locationlist = onelocationlist
            else:
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

#provide query to nepal map
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
    barlocations = []
    for location in countlist:
        if location['location'].lower() in ktm_location:
            ktm_death += location['death']
            ktm_injury += location['injury']
            ktm_count += location['count']
            barlocations.append({'location': 'Kathmandu', 'injury': ktm_injury, 'value': ktm_death})
            maplocations.append({'location': 'Kathmandu', 'injury': ktm_injury, 'value': ktm_death, 'count': ktm_count})
        elif location['location'].lower() in ltp_location:
            ltp_death += location['death']
            ltp_injury += location['injury']
            ltp_count += location['count']
            barlocations.append({'location': 'Lalitpur', 'injury': ltp_injury, 'value': ltp_death})
            maplocations.append({'location': 'Lalitpur', 'injury': ltp_injury, 'value': ltp_death, 'count': ltp_count})
        elif location['location'].lower() in bkt_location:
            bkt_death += location['death']
            bkt_injury += location['injury']
            bkt_count += location['count']
            maplocations.append({'location': 'Bhaktapur', 'injury': bkt_injury, 'value': bkt_death, 'count': bkt_count})
            barlocations.append({'location': 'Bhaktapur', 'injury': bkt_injury, 'value': bkt_death})
        elif location['location'].lower() in outside_location:
            maplocations.append({'location': location['location'].capitalize(), 'value': location['death'],
                             'injury': location['injury'],'count': location['count']})
            barlocations.append({'location': location['location'].capitalize(), 'value': location['death'],
                                 'injury': location['injury']})
        else:
            pass
    return (barlocations, maplocations)

# def vehicletypecheck(query):
#     newquery = query.filter(vehicle_type__icontains=search)
#main function
def location(request):
    listoflocation, ktmlocationlist, ltplocationlist, bktlocationlist = selectparameters()
    vehicle_types = ['two wheeler', 'three wheeler' , 'four wheeler']
    #all necessary queries
    yearlist = rssdata.objects.values('year').order_by('year').annotate(count=Count('year'))
    locationlist = rssdata.objects.values('location').order_by('location').annotate(count=Count('location')).annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no'))
    tablelocationlist = rssdata.objects.all().values('location', 'year', 'month', 'vehicleone',
                                                   'vehicletwo', 'date').order_by('location').annotate(count=Count('location')).annotate(deathno=Sum('death_no')).annotate(injuryno=Sum('injury_no'))
    vehiclelist = rssdata.objects.values('vehicleone').order_by('vehicleone').annotate(count=Count('vehicleone'))
    vehiclelisttwo = rssdata.objects.values('vehicletwo').order_by('vehicletwo').annotate(count=Count('vehicletwo'))
    monthlist = rssdata.objects.values('month').order_by('month').annotate(count=Count('month'))
    vehicletypelist = rssdata.objects.values('vehicle_type')
    datelistinc = rssdata.objects.values('date').order_by('date').annotate(count=Count('date'))
    date = datelistinc[0]['date']

    three_wheeler = ['tempo', 'three-wheeler', 'three wheeler']

    two_wheeler = ['bike', 'scooter', 'scooty', 'motorbike', 'motorcycle', 'two-wheeler', 'two wheeler', 'moped']

    four_wheeler = ['bus', 'car', 'truck', 'tipper', 'zeep', 'container', 'SUV', 'tractor', 'moped', 'lorry',
        'minivan', 'minibus', 'trolley', 'four-wheeler', 'four wheeler', 'jeep']

    #initializing list
    vehicledata = []
    tablelocation = []
    vehicletype = []
    vehicletwowheeler =[]
    vehiclethreewheeler = []
    vehiclefourwheeler = []

    for newv in vehicletypelist:
        for v in vehicle_types:
            if v in newv['vehicle_type']:
                if v not in vehicletype:
                    vehicletype.append(v)

    #if select option doesnot match show data to user
    for loc in tablelocationlist:
        if len(loc['location']) >2:
            tablelocation.append({'location': loc['location'].capitalize(), 'deathno': loc['deathno'],
                             'injuryno': loc['injuryno'], 'date': loc['date'], 'year': loc['year'], 'month': loc['month'],
                                  'vehicleone': loc['vehicleone'], 'vehicletwo': loc['vehicletwo']})

    #provide data to select tag in vehicle column
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

    for vdata in vehicledata:
        if vdata in two_wheeler:
            vehicletwowheeler.append(vdata)
        if vdata in three_wheeler:
            vehiclethreewheeler.append(vdata)
        if vdata in four_wheeler:
            vehiclefourwheeler.append(vdata)
    valueslist = []
    todaydate = datetime.datetime.now().date()
    # working in search query
    if request.POST:
            vehicletypeinfo = request.POST.get('vehicletype', None)
            yearinfo =  request.POST.get('year', None)
            locationinfo = request.POST.get('location', None)
            monthinfo = request.POST.get('month', None)
            valueslist.append({'vehicletwoinfo': request.POST.get('vehicle_two', None),
                               'vehiclethreeinfo': request.POST.get('vehicle_three', None),
                               'vehiclefourinfo': request.POST.get('vehicle_four', None),
                               'vehicletypeinfo': request.POST.get('vehicletype', None),
                               'yearinfo': request.POST.get('year', None),
                               'locationinfo': request.POST.get('location', None),
                               'ktmlocationinfo': request.POST.get('ktmlocation', None),
                               'ltplocationinfo': request.POST.get('ltplocation', None),
                               'datefrom' : request.POST.get('from', None),
                               'dateto': request.POST.get('to', None),
                               'bktlocationinfo': request.POST.get('bktlocation', None),
                               'monthinfo': request.POST.get('month', None)})

            newlocationlist, filterlocation, information, totalno, countlist = getqueries(valueslist, ktmlocationlist,ltplocationlist,bktlocationlist)

            barlocations , maplocations = finalquery(countlist)
            max = 0
            for location in maplocations:
                if location['count'] > max:
                    max = location['count']
            diffList = []
            diffcount = []
            # for location in maplocations:
            for i in range(0, len(maplocations)):
                diff = max - maplocations[i]['count']
                if diff not in diffcount:
                    if diff > 9:
                        diff = 10
                        diffcount.append(diff)
                        diffList.append({'difference': diff, 'counts': maplocations[i]['count']})
                    else:
                        diffcount.append(diff)
                        diffList.append({'difference': diff, 'counts': maplocations[i]['count']})

            if (len(filterlocation) == 0):
                context = {
                    'locationlist': tablelocation,
                    'listoflocation': listoflocation,
                    'ktm_location': ktmlocationlist,
                    'ltp_location': ltplocationlist,
                    'bkt_location': bktlocationlist,
                    'monthlist': monthlist,
                    'vehicletwo': vehicletwowheeler,
                    'vehiclethree': vehiclethreewheeler,
                    'vehiclefour': vehiclefourwheeler,
                    'yearlist': yearlist,
                    'monthvalue': monthinfo,
                    'yearvalue': yearinfo,
                    'vehicletype': vehicletype,
                    'locationvalue': locationinfo,
                    'vehiclevalue': vehicletypeinfo,
                    'today':todaydate,
                    'start': date,
                }
                return render(request, "findlocation.html", context)
            for location in barlocations:
                if location['value']==0 and location['injury'] ==0:
                    context = {
                        'locationinfos': newlocationlist,
                        'listoflocation': listoflocation,
                        'ktm_location': ktmlocationlist,
                        'ltp_location': ltplocationlist,
                        'bkt_location': bktlocationlist,
                        'monthlist': monthlist,
                        'totalno': totalno,
                        'vehicletwo': vehicletwowheeler,
                        'vehiclethree': vehiclethreewheeler,
                        'vehiclefour': vehiclefourwheeler,
                        'yearlist': yearlist,
                        'info': information,
                        'monthvalue': monthinfo,
                        'vehicletype': vehicletype,
                        'yearvalue': yearinfo,
                        'vehiclevalue': vehicletypeinfo,
                        'locationvalue': locationinfo,
                        'today': todaydate,
                        'start': date,
                        'checkparam': "none",
                    }
                    return render(request, "location.html", context)
            context = {
                'differences': diffList,
                'max': max,
                'locationinfos': newlocationlist,
                'location_data': json.dumps(barlocations),
                'listoflocation': listoflocation,
                'ktm_location': ktmlocationlist,
                'ltp_location': ltplocationlist,
                'bkt_location': bktlocationlist,
                'monthlist': monthlist,
                'totalno': totalno,
                'vehicletwo': vehicletwowheeler,
                'vehiclethree': vehiclethreewheeler,
                'vehiclefour': vehiclefourwheeler,
                'yearlist': yearlist,
                'info': information,
                'monthvalue': monthinfo,
                'vehicletype': vehicletype,
                'yearvalue': yearinfo,
                'vehiclevalue': vehicletypeinfo,
                'locationvalue': locationinfo,
                'newdata': json.dumps(maplocations),
                'today': todaydate,
                'start': date
            }
            return render(request, "location.html", context)



    totalno = len(locationlist)
    barlocations, maplocations = finalquery(locationlist)

    max = 0
    for location in maplocations:
        if location['count']>max:
            max = location['count']
    diffList = []
    diffcount =[]
    # for location in maplocations:
    for i in range(0, len(maplocations)):
        diff = max - maplocations[i]['count']
        if diff not in diffcount:
            if diff > 9:
                diff = 10
                diffcount.append(diff)
                diffList.append({'difference': diff, 'counts': maplocations[i]['count']})
            else:
                diffcount.append(diff)
                diffList.append({'difference': diff, 'counts': maplocations[i]['count']})
    print diffList


    context = {
        'differences': diffList,
        'max': max,
        'locationinfos': tablelocation,
        'location_data': json.dumps(barlocations),
        'listoflocation': listoflocation,
        'ktm_location': ktmlocationlist,
        'ltp_location': ltplocationlist,
        'bkt_location' : bktlocationlist,
        'monthlist' : monthlist,
        'totalno': totalno,
        'vehicletwo': vehicletwowheeler,
        'vehiclethree': vehiclethreewheeler,
        'vehiclefour': vehiclefourwheeler,
        'yearlist': yearlist,
        'vehicletype': vehicletype,
        'newdata': json.dumps(maplocations),
        'today': todaydate,
        'start' : date,
        'locationvalue': "Kathmandu",
    }
    return render(request, "location.html", context)

#query for kathmandu valley map
def index(request):
    location = rssdata.objects.values('location').order_by('location').annotate(death=Sum('death_no')).annotate(injury=Sum('injury_no')).annotate(count=Count('location'))
    totalno = rssdata.objects.values('date').aggregate(total=Count('date'))
    latitude = []

    for locations in location:
        if locations['location'] is not None:
            if (len(locations['location']) > 2):
                loc = locations['location']
                g = geocoder.google(loc)
                if g.lat is not None:
                    latitude.append(
                        {'location': loc, 'latitude': g.lat, 'longitude': g.lng, 'death': locations['death'],
                         'injury': locations['injury'], 'count': locations['count']})

                # geolocator = Nominatim()
                # g = geolocator.geocode(loc)
                # latitude.append({'location': loc, 'latitude': g.latitude, 'longitude': g.longitude, 'death': locations['death'],
                #                      'injury': locations['injury']})

    print(latitude)

    context = {
        # 'personal_detail': json.dumps(datas),
        # 'data': data,
        'latitude': latitude,
        'totalno': totalno,
    }
    return render(request, "heatmap.html", context)


def searchnumber(request):
    tablevehiclelist = rssdata.objects.all().values('vehicle_no').order_by('vehicle_no')

    tablevehicle = []
    vehiclenolist = []
    vehicletable = []
    # if vehicle no search is not found then data base is shown
    for loc in tablevehiclelist:
        if len(loc['vehicle_no']) > 2:
            tablevehicle.append({'vehicleno': loc['vehicle_no']})

    for vehicle in tablevehicle:
        newv = vehicle['vehicleno']
        newv = unicode(newv).encode('ascii')
        word = re.findall(r'[A-Za-z]{1,2}\s[0-9]{0,1}\s[A-Za-z]{2,4}\s[0-9]{2,4}', newv)
        for w in word:
            if w not in vehiclenolist:
                vehiclenolist.append(w)

    if request.POST:
        search =  request.POST.get('query', None)
        if search in vehiclenolist:
            queryset_list = rssdata.objects.filter(vehicle_no__icontains=search).values('location', 'date', 'death_no',
                                                                                    'injury_no', 'vehicle_no')
            context = {
                'location_data': queryset_list,
                'search': search,
            }
            return render(request, "search.html", context)
        else:
            queryset_list = rssdata.objects.filter(vehicle_no__icontains=search).values('vehicle_no')
            for vehicle in vehiclenolist:
                for v in queryset_list:
                    if vehicle in v['vehicle_no']:
                        vehicletable.append(vehicle)
            if len(queryset_list) == 0:
                context = {
                    'nodetail': search,
                }
                return render(request, "search.html", context)
            else:
                context = {
                    'vehicledata': vehicletable,
                    'search': search,
                }
                return render(request, "search.html", context)

    return render(request, "search.html")