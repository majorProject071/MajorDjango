from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

from forms import NameForm
from methods import *


def index(request):
    initial_check()
    news_list = rssdata.objects.all().order_by("-id")
    page = request.GET.get('page', 1)

    paginator = Paginator(news_list, 5)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    index = news.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 4 if index >= 4 else 0
    end_index = index + 4 if index <= max_index - 4 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'index.html', {'news': news, 'page_range': page_range})

#
# def blog(request):
#     paginator = Paginator(Blog.objects.all(), 1)
#
#     try:
#         page = int(request.GET.get('page', '1'))
#     except:
#         page = 1
#
#     try:
#         blogs = paginator.page(page)
#     except(EmptyPage, InvalidPage):
#         blogs = paginator.page(1)
#
#     index = blogs.number - 1  # edited to something easier without index
#     max_index = len(paginator.page_range)
#     start_index = index - 3 if index >= 3 else 0
#     end_index = index + 3 if index <= max_index - 3 else max_index
#     page_range = list(paginator.page_range)[start_index:end_index]
#
#     return render(request, 'blogs.html', {
#         'blogs': blogs,
#         'page_range': page_range,
#     })


def extraction(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            extracted_data = data['news_link']
            try:
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
            except:
                pass
    else:
        form = NameForm()

    return render(request, 'extraction.html', {'form': form})


def about_us(request):
    return render(request, 'about_us.html')


def contact_us(request):
    return render(request, 'contact_us.html')