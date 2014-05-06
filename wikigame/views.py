from django.shortcuts import render

from wikigame.link_extraction import get_links


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def article(request, article):
    context = {'article': article, 'links': get_links(article, 'en')}

    return render(request, 'article.html', context)
