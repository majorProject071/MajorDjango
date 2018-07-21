from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from forms import NameForm
from .models import *
from methods import initial_check, extract_info, save_extracted_info

def index(request):
    initial_check()
    news_list = rssdata.objects.all().order_by("-id")
    page = request.GET.get('page', 1)

    paginator = Paginator(news_list, 4)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'news': news})


def extraction(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            extracted_data = extract_info(data['news_text'])
            # If you want to save the input news
            story = save_extracted_info(data['news_title'], data['news_text'], extracted_data)
        return render(request, 'extraction.html', {'form': form,
                                                   'news_id': story.pk,
                                                   'article': rssdata.objects.get(pk=story.pk)})
    else:
        form = NameForm()

    return render(request, 'extraction.html', {'form': form})


def about_us(request):
    return render(request, 'about_us.html')


def contact_us(request):
    return render(request, 'contact_us.html')