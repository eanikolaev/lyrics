from django.conf.urls import patterns, url

urlpatterns = patterns('',
     url(r'^$', 'lyrics.views.index', name='index'),
)
