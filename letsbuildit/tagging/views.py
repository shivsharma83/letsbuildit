from django.http import HttpResponse
from django.shortcuts import render
from tagging import models, refreshtag, forms, updatetags, svntagging

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
        return render(request, 'tagit.html', {'tags' : tagslist})

def tagged(request):
	results = {}
	tagslist = models.tag_history.objects.all()
	for tag in tagslist:
		if tag.componentname().__unicode__() in request.POST:
			if request.POST[tag.componentname().__unicode__()] != "":
				result = updatetags.updategittag(tag.componentname().__unicode__(), request.POST[tag.componentname().__unicode__()], "Adding Tag " + request.POST[tag.componentname().__unicode__()])
				if result == 'Pass':
					results[tag.componentname().__unicode__()] = request.POST[tag.componentname().__unicode__()]
				else:
					results[tag.componentname().__unicode__()] = "Failed to tag!!!"
			else:
				results[tag.componentname().__unicode__()] = "No New Tag!!!"

	taglist = refreshtag.addtagsindb("all")
	return render(request, 'tagged.html', {'results' : results})

def svntagging(request):

	return render(request, 'svntagging.html')

def svntagged(request):

	tag_dir   = request.POST['tagdir']
	message   = request.POST['message']
	comp_type = request.POST['comp_type']
	tag       = request.POST['tag']

	if tag_dir != "" and tag !="" :
		status_dir = updatetags.tag_dir(tag_dir, message, comp_type)	
		if status_dir is True:
			status, alltags = updatetags.createtag(tag,tag_dir, message, comp_type)
		else:
			status = "Couldn't create tagdir and Tag"
			alltags= "Nothing"

	return render(request, 'svntagged.html' , {'status' : status, 'alltags': alltags})
