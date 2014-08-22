from django.conf.urls import patterns, include, url

from tagging import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^vcs/$', views.vcs, name='vcs'),
    url(r'^components/$', views.components, name='components'),
    url(r'^latesttags/$', views.tags, name='tags'),
    url(r'^refreshtags/$', views.refreshtags, name='refreshtags'),
    url(r'^tagit/$', views.tagit, name='tagit'),
    url(r'^tagged/$', views.tagged, name='tagged'),
    url(r'^svntagging/$', views.svntagging, name='svntagging'),
    url(r'^svntagged/$', views.svntagged, name='svntagged'),
)
