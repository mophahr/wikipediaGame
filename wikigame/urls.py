from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

urlpatterns = patterns('',
    url(r'^$', 'wikigame.views.home', name='home'),
    url(r'^%s$' % _('about'), 'wikigame.views.about', name='about'),
    url(r'^%s/(.*)$' % _('article'), 'wikigame.views.article', name='article'),
    url(r'^%s/(.*)$' % _('start'), 'wikigame.views.start_page', name='start_page'),
    url(r'^%s$' % _('end'), 'wikigame.views.end_page', name='end_page'),

    url(r'^%s/data$' % _('end'), 'wikigame.views.compute_histogram_json', name='end_page_json'),
)
