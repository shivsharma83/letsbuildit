import sh
from tempfile import *
import os
from git import *
import re
from tagging import models
from time import strptime, mktime
from datetime import datetime
from shutil import rmtree 

def addtagsindb(components):

	#Define dictionaries those will be used later 
	tagslist = {}

	try:
		tempdir = mkdtemp(prefix="tagging_",dir="/tmp")
	except:
		raise

	# Change to that directory

	os.chdir(tempdir)
	# Get the list of all components and its attributes

	componentlist = models.components.objects.filter(version_control="git")
	for component in componentlist:
		tagdate = {}
        # Get Version control credentials
		vcs  = models.vc_credentials.objects.filter(version_control="git").values()
		user = vcs[0]['userid']
		passwd = vcs[0]['password']

		repo_credentials = component.repo()[:8] + user + ':' + passwd + '@' + component.repo()[8:]
		try:
			rep = sh.git.clone("-b", component.comp_branch() , repo_credentials)
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

        #  Add Detials to dictionary of dictionary 
		tagslist[component.__unicode__()] = tagdate

		if latesttag in tagdate:

			if tagdate[latesttag].strip() == '':
				when = datetime.now()
			else:
				when = datetime.fromtimestamp(mktime(strptime(tagdate[latesttag].strip())))

			ctrl = models.tag_history(component_name=component, tag=latesttag, datetime=when, latest_tag=True)
		        ctrl.save()
	# remove temp directories
	try:
		os.chdir("/tmp")
		rmtree(tempdir[5:])
	except:
		raise OSError

	# return the dictionary of tags and its dates with component as key
	return tagslist

if __name__ == '__main__':
	addtagsindb("all")
