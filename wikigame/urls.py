from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'wikigame.views.home', name='home'),
)
