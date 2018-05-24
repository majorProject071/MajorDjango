from django.shortcuts import render, get_object_or_404
from .models import *

def index(request):
    return render(request, 'index.html',
                  context={'news': rssdata.objects.all()})