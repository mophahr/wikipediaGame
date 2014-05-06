from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

urlpatterns = patterns('',
    url(r'^$', 'wikigame.views.home', name='home'),
    url(r'^%s$' % _('about'), 'wikigame.views.about', name='about'),
    url(r'^%s/(.*)$' % _('article'), 'wikigame.views.article', name='article'),
)
