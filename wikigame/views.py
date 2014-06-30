import json

from django.db.models import Min
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from wikigame import link_extraction
from wikigame.models import Problem, Result, create_problems


def get_links(article_name, language):
    return link_extraction.filter_links(link_extraction.get_links(article_name, language))


def home(request):
    create_problems()
    problems = Problem.objects.all()

    return render(request, 'home.html', {'problems': problems})


def about(request):
    return render(request, 'about.html')


def article(request, article):
    # validate entry (it must come from start_page to flush session).
    if 'path' not in request.session:
        # todo: message the user saying it must start from a challenge.
        return redirect('home')

    previous_article = request.session['path'][-1]

    # if it is the same, we consider it a reload and do nothing
    if article != previous_article:
        # ensure the article is valid (this article is accessible from the previous one)
        # this avoids cheating by changing the url (principle that HTML requests are anonymous)
        #if article not in get_links(previous_article, 'en'):
        #    # todo: message the user saying the current article is X
        #    return redirect('article', previous_article)

        # everything good: add it to the path and force the session to be saved.
        request.session['path'].append(article)
        request.session.modified = True

        # check if we have reached the final article
        problem = Problem.objects.get(id=request.session['problem'])
        if article == problem.end:
            return redirect('end_page')

    links = get_links(article, 'en')

    context = {'article': article, 'links': links, 'path': request.session['path']}
    return render(request, 'article.html', context)


def start_page(request, problem_id):
    create_problems()
    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        # todo: alert user
        return redirect('home')

    article = problem.start

    request.session.flush()
    request.session['problem'] = problem.id
    request.session['path'] = [article]

    context = {'article': article, 'links': get_links(article, 'en')}

    return render(request, 'article.html', context)


def end_page(request):

    problem = Problem.objects.get(id=request.session['problem'])

    best = Result.objects.aggregate(min=Min('path_length'))['min']

    result = Result.objects.create(problem=problem,
                                   path_length=len(request.session['path']) + 1)

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


def compute_histogram_json(request):

    histogram = {'values': [], 'key': _('histogram of path length')}
    for path_length in range(100):
        result = Result.objects.filter(path_length=path_length).count()
        if result:
            histogram['values'].append(
                {'x': path_length,
                 'y': result})

    return HttpResponse(json.dumps([histogram]), content_type="application/json")
