#import necessary headers
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Sum, Max
from django.shortcuts import render
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.db import connections
from geopy.geocoders import Nominatim

from .models import *
import json
from news_extraction.models import *
from django.core import serializers
from django.http import JsonResponse

def index (request):
    location = rssdata.objects.values_list('location', flat=True)
    data = rssdata.objects.values('location').annotate(total=Sum('death_no'))
    totalno = rssdata.objects.values('date').aggregate(total=Count('date'))
    datas = list(data)
    print datas
    latitude = []

    for locations in location:
        if locations is not  None:
            if(len(locations)>2):
                loc = locations
                geolocator = Nominatim()
                locations = geolocator.geocode(loc)
                locations = (locations.latitude, locations.longitude)
                latitude.append(locations)
    print(latitude)

    context={
            'personal_detail': json.dumps(datas),
            'data':data,
            'latitude':latitude,
            'totalno': totalno,
    }
    return render(request, "heatmap.html", context)


def districts(request):
    location = rssdata.objects.values_list('location', flat=True)
    print(location)
    return render(request, "districts.html")

def check(request):
    return render(request, "check.html")

def bar (request):
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
