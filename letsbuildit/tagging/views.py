from django.http import HttpResponse
from django.shortcuts import render
from tagging import models

# Create your views here.

def index(request):
	return render(request, 'home_page.html')

def vcs(request):
	vcslist = models.vc_credentials.objects.all()
	return render(request, 'vcs.html', {'vcslist' : vcslist})	

def components(request):
        componentlist = models.components.objects.all()
        return render(request, 'components.html', {'components' : componentlist})

def tags(request):
#	refreshtag.addtagsindb("all")
	tagslist = models.tag_history.objects.all()
        return render(request, 'latesttags.html', {'tags' : tagslist})
