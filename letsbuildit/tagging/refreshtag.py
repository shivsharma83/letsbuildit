from sh import git , cd 
from tempfile import *
from os import *
from tagging import models

def addtagsindb(components):
	if components == "all":
		'''do this'''
		try:
			tempdir = tempdir = mkstemp(prefix="tagging_",dir="/tmp") 
			temp = tempdir[1]
		except:
			raise

		cd(temp)
		componentlist = models.components.objects.all()
		for component in componentlist:
			if not os.path.exists(temp/component):
				try:
					os.makedirs(temp/component)
				except:
					raise
			if component.vc == "git":
				vcs  = models.vc_credentials.objects.filter(version_control='git')
				user = vcs[1]
				passwd = vcs[2]
					
			cd(temp/component)
			repo_credentials = component.repo[:8] + user + ':' + passwd + '@' + component[8:]
			try:
				repo = git.clone(repo_credentials)
			except:
				raise
			 
		
	else:
		'''do that'''

