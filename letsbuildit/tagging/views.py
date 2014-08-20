from django.http import HttpResponse
from django.shortcuts import render
from tagging import models, refreshtag, forms

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
	tagslist = models.tag_history.objects.all()
        return render(request, 'latesttags.html', {'tags' : tagslist})

def refreshtags(request):
        tagslist = refreshtag.addtagsindb("all")
        return render(request, 'refresh_tags.html', {'tagslist' : tagslist})

def tagit(request):
	tagslist = models.tag_history.objects.all()
	###render(request, 'tagit.html', {'tags' : tagslist})
	formset = forms.TagitFormSet(request.POST)
        return render(request, 'tagit.html', {'tags' : tagslist, 'formset' : formset})



