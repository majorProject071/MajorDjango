from forms import NameForm

from django.shortcuts import render
from .models import *
from methods import initial_check, extract_info, save_extracted_info

def index(request):
    initial_check()
    return render(request, 'index.html',
                  context={'news': rssdata.objects.all().order_by("-id")})


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