from django.conf.urls import patterns, include, url

from tagging import views

urlpatterns = patterns('',
    url(r'^$', views.vcs, name='vcs')
)
