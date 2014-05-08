from django.shortcuts import render, redirect

from wikigame.link_extraction import get_links


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def article(request, article):
    # validate entry (it must come from start_page to flush session).
    if 'path' not in request.session:
        # message the user saying it must start from a challenge.
        return redirect('home')

    previous_article = request.session['path'][-1]

    # if it is the same, we consider it a reload and do nothing
    if article != previous_article:

        # ensure the article is valid (this article is accessible from the previous one)
        # this avoids cheating by changing the url (principle that HTML requests are anonymous)
        if article not in get_links(previous_article, 'en'):
            # message the user saying the current article is X
            return redirect('article', previous_article)

        # everything good: add it to the path and force the session to be saved.
        request.session['path'].append(article)
        request.session.modified = True

    context = {'article': article, 'links': get_links(article, 'en'), 'path': request.session['path']}
    return render(request, 'article.html', context)


def start_page(request, article):
    request.session.flush()
    request.session['path'] = [article]

    context = {'article': article, 'links': get_links(article, 'en')}

    return render(request, 'article.html', context)