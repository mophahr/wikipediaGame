import json

from django.db.models import Min
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib import messages

from wikigame import link_extraction
from wikigame.link_extraction import NoLinksError
from wikigame.models import Problem, Result, create_problems


game_related_session_keys = ['problem', 'path']


def flush_game_session(session):
    for key in game_related_session_keys:
        if key in session:
            session.pop(key)


def get_links(article_name):
    try:
        de_links = link_extraction.filter_links(link_extraction.get_links(article_name, 'de'))
    except NoLinksError:
        return []

    #return sorted(list(de_links.union(en_links)))
    return sorted(de_links)


def home(request):
    flush_game_session(request.session)
    create_problems()
    problems = Problem.objects.all()

    return render(request, 'home.html', {'problems': problems})


def about(request):
    return render(request, 'about.html')


def article(request, article):
    # validate entry (it must come from start_page to flush session).
    if 'path' not in request.session:
        messages.warning(request, _('You were redirected to main page: '
                                    'you must start from it.'))
        return redirect('home')

    previous_article = request.session['path'][-1]
    problem = Problem.objects.get(id=request.session['problem'])
    links = get_links(article)

    # empty list means the article does not exist (the red links in wiki).
    # in this case we redirect
    if not links:
        messages.warning(request, _('You tried an article without links :/. '
                                    'we gave you the chance to try other article.'))
        return redirect('article', previous_article)

    # if it is the same, we consider it a reload and do nothing
    if article != previous_article:
        # ensure the article is valid (this article is accessible from the previous one)
        # this avoids cheating by changing the url (principle that HTML requests are anonymous)
        if article not in get_links(previous_article):
            messages.warning(request, _('You tried an article that is not '
                                        'connected to your path: '
                                        'we have redirected you to your path.'))
            return redirect('article', previous_article)

        # everything good: add it to the path and force the session to be saved.
        request.session['path'].append(article)
        request.session.modified = True

        # check if we have reached the final article
        if article == problem.end:
            return redirect('end_page')

    context = {'article': article,
               'links': links,
               'path': request.session['path'],
               'problem': problem}
    return render(request, 'article.html', context)


def start_page(request, problem_id):
    create_problems()
    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        messages.warning(request, _('This problem doesn\'t seem to exist. '
                                    'we have redirected you to the main page.'))
        return redirect('home')

    article = problem.start

    flush_game_session(request.session)
    request.session['problem'] = problem.id
    request.session['path'] = [article]

    context = {'article': article, 'links': get_links(article), 'path': request.session['path']}

    return render(request, 'article.html', context)


def end_page(request):
    if 'problem' not in request.session:
        return redirect('home')
    problem = Problem.objects.get(id=request.session['problem'])

    # the game only ends when the user reaches the end!
    if problem.end != request.session['path'][-1]:
        return redirect('article', request.session['path'][-1])

    best = Result.objects.aggregate(min=Min('path_length'))['min']

    result = Result.objects.create(problem=problem,
                                   path_length=len(request.session['path']))

    # after the user ends, the game is restarted (so the user cannot use
    # back and finish again)
    flush_game_session(request.session)

    ## rank the results with equal ranks if they have the same path_length
    results = Result.objects.order_by('path_length', '-time')[:20]
    current = 0
    current_result = results[0]
    for r in results:
        if r.path_length != current_result:
            current += 1
            current_result = r.path_length
        r.rank = current

    return render(request, 'end.html', {'result': result,
                                        'problem': problem,
                                        'best': best,
                                        'results': results})


def compute_histogram_json(request, problem_id):

    histogram = {'values': [], 'key': _('histogram of path length')}
    for path_length in range(100):
        result = Result.objects.filter(problem__id=problem_id,
                                       path_length=path_length).count()
        if result:
            histogram['values'].append(
                {'x': path_length,
                 'y': result})

    return HttpResponse(json.dumps([histogram]), content_type="application/json")
