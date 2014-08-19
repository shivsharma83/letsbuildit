from tempfile import *
import os
from git import *
import re
from tagging import models

def addtagsindb(components):
        print("I am in")	
	tagndate = []
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

		if component.vc == "git":
			vcs  = models.vc_credentials.objects.filter(version_control='git')
			user = vcs[1]
			passwd = vcs[2]
					
		repo_credentials = component.repo[:8] + user + ':' + passwd + '@' + component[8:]
		try:
			repo = git.clone(repo_credentials)
		except:
			raise
	
	# Chagne to the repo directory 
			
		os.chdir(component)
		repo_path = temp + '/' + component 	
				
		repo = Repo(repo_path)
		git = repo.git
			
		taglist = git.for_each_ref(sort="refname", format='%(refname) - %(taggerdate)')
		regstring = re.compile('refs/tags/*')

		for t in taglist.rsplit("\n"):
			if regstring.match(t):
				tempstr = re.sub('\+[0-9]+','',re.sub(regstring,'',t))
				tagdate[tempstr.split("-")[0]] = tempstr.split("-")[1]
				
		print(tagdate)

if __name__ == '__main__':
	print("i m in main")
	addtagsindb("all")
