from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from forms import NameForm
from methods import *


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
            extracted_data = data['news_link']
            link, news , title = manual_extract(extracted_data)

            # If you want to save the input news
            oldlinks = rssdata.objects.values_list('link', flat=True)

            if link not in oldlinks:
                id = extract(link, news, title)
                return render(request, 'extraction.html', {'form': form,
                                                           'news_id': id,
                                                           'article': rssdata.objects.get(pk=id)})
            else:
                print link
                id = 5
                return render(request, 'extraction.html', {'form': form,
                                                           'news_id': id,
                                                           'article': rssdata.objects.get(link=link)})
    else:
        form = NameForm()

    return render(request, 'extraction.html', {'form': form})


def about_us(request):
    return render(request, 'about_us.html')


def contact_us(request):
    return render(request, 'contact_us.html')