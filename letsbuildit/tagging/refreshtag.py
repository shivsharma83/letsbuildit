import sh
from tempfile import *
import os
from git import *
import re
from tagging import models
from time import strptime, mktime
from datetime import datetime

def addtagsindb(components):
	tagdate = {}
	if components == "all":
		# Create a temp directory to download git repos
		try:
			tempdir = mkdtemp(prefix="tagging_",dir="/tmp") 
		except:
			raise

	# Change to that directory

	os.chdir(tempdir)
	# Get the list of all components and its attributes 

	componentlist = models.components.objects.all()
	for component in componentlist:
	
        # Get Version control credentials 
#		if component.vc() == "git":
		vcs  = models.vc_credentials.objects.filter(version_control="git").values()
		user = vcs[0]['userid']
		passwd = vcs[0]['password']
		
		repo_credentials = component.repo()[:8] + user + ':' + passwd + '@' + component.repo()[8:]
		try:
			rep = sh.git.clone(repo_credentials)
		except:
			raise
	# Chagne to the repo directory 
			
	#	os.chdir(component.__unicode__())
		repo_path = tempdir + '/' + component.__unicode__()
				
		repo = Repo(repo_path)
		git = repo.git
			
		taglist = git.for_each_ref(sort="refname", format='%(refname) - %(taggerdate)')
		regstring = re.compile('refs/tags/*')

		for t in taglist.rsplit("\n"):
			if regstring.match(t):
				tempstr = re.sub('\+[0-9]+','',re.sub(regstring,'',t))
				tagdate[tempstr.split(" - ")[0]] = tempstr.split(" - ")[1]

	# Find latst tag and label it as latest
		latesttag = git.describe("--tag")
		if latesttag in tagdate:

			if tagdate[latesttag].strip() == '':
				when = datetime.now()
			else:
				when = datetime.fromtimestamp(mktime(strptime(tagdate[latesttag].strip())))

			ctrl = models.tag_history(component_name=component, tag=latesttag, datetime=when, latest_tag=True)
			if not models.tag_history.objects.filter(component_name=component.__unicode__()):
				ctrl.save()


if __name__ == '__main__':
	addtagsindb("all")
