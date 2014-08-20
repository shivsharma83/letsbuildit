import sh
from tempfile import *
import os
from git import *
import re
from tagging import models
from time import strptime, mktime
from datetime import datetime

def updategittag(component, newtag , message):
	try:
		tempdir = mkdtemp(prefix="tagging_",dir="/tmp")
	except:
		raise

	# Change to that directory
	os.chdir(tempdir)

	# Get the component and its attributes
	comp = models.components.objects.filter(component_name=component, version_control="git").values()
        # Get Version control credentials
	vcs  = models.vc_credentials.objects.filter(version_control="git").values()
	user = vcs[0]['userid']
	passwd = vcs[0]['password']

	repo_credentials = comp[0]['repo_path'][:8] + user + ':' + passwd + '@' + comp[0]['repo_path'][8:]
	branch = comp[0]['branch']
	try:
		rep = sh.git.clone("-b", branch , repo_credentials)
	except:
		raise

	repo_path = tempdir + '/' + comp[0]['component_name']

	repo = Repo(repo_path)
	git = repo.git

	if newtag in git.tag().rsplit("\n"):
		status = "Fail"	
	else:
		git.tag(newtag,m=message)
	        git.remote("add","upstream",repo_credentials)
		git.push("upstream",newtag,"--force")
		status = "Pass"

	return status
