from django.shortcuts import render

from wikigame.link_extraction import get_links


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def article(request, article):
    context = {'article': article, 'links': get_links(article, 'en'), 'path': request.session['path']}

    if article != request.session['path'][-1]:
        request.session['path'].append(article)
        request.session.modified = True

    return render(request, 'article.html', context)


def start_page(request, article):
    request.session.flush()
    request.session['path'] = [article]

    context = {'article': article, 'links': get_links(article, 'en')}

    return render(request, 'article.html', context)