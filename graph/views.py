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

from .models import *
import json
from django.core import serializers
from django.http import JsonResponse

def index (request):
    data = News.objects.values('Year').annotate( total=Sum('Death'))
    datas = list(data)
    context={
            'personal_detail': datas,
            'data':data,
    }
    return render (request, "graph.html",context)

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