from sh import svn, ErrorReturnCode_1, ErrorReturnCode
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


def tag_dir(newtagdir, message, comp_type):

        vcs      = models.vc_credentials.objects.filter(version_control="svn").values()
        username = vcs[0]['userid']
        passwd   = vcs[0]['password']
	message  = "'" + message + "'"
        if comp_type == "non-shared":
                comp = models.components.objects.filter(component_name="SVN", version_control="svn").values()
        elif comp_type == "shared":
                comp = models.components.objects.filter(component_name="SVN2", version_control="svn").values()
        else:
                comp = models.components.objects.filter(component_name="SVN", version_control="svn").values()

        # this is just for shivlinux to recoganize .. not to go in prod
        svn_repo = comp[0]['repo_path'][:16] + comp[0]['repo_path'][30:] + "/tags/" + newtagdir
        #svn_repo = comp[0]['repo_path']

	try:
		dirstatus = svn.ls(svn_repo, "--no-auth-cache", "--non-interactive", "--username="+username, "--password="+passwd)
		if dirstatus != "":
			#Directory exists 
			status = True
			return status

	except ErrorReturnCode_1:
		dirstatus = False

	if dirstatus is False:
        	try:	
        		status = svn.mkdir(svn_repo,"--no-auth-cache", "--non-interactive", "--username="+username, "--password="+passwd, "--parents","-m "+message)
			status = True
		except ErrorReturnCode:
			status = False

        #Save this tagdir as latest tag
        if status is True: 
                latesttag = newtagdir
                when = datetime.now()
		if comp_type == "non-shared":
			ctrl = models.tag_history(component_name=models.components.objects.get(component_name="SVN"), tag=latesttag, datetime=when, latest_tag=True)
		else:
			ctrl = models.tag_history(component_name=models.components.objects.get(component_name="SVN2"), tag=latesttag, datetime=when, latest_tag=True)

                ctrl.save()

        return status

def createtag(newtag, newtagdir, message, comp_type):

        vcs      = models.vc_credentials.objects.filter(version_control="svn").values()
        username = vcs[0]['userid']
        passwd   = vcs[0]['password']
	message  = "'" + message + "'"

        if comp_type == "non-shared":
                comp = models.components.objects.filter(component_name="SVN", version_control="svn").values()
        elif comp_type == "shared":
                comp = models.components.objects.filter(component_name="SVN2", version_control="svn").values()
        else:
                comp = models.components.objects.filter(component_name="SVN", version_control="svn").values()

        # this is just for shivlinux to recoganize .. not to go in prod
        svn_repo = comp[0]['repo_path'][:16] + comp[0]['repo_path'][30:]

       # svn_repo = comp[0]['repo_path']
        branch   = comp[0]['branch']
        # Create tag and get the list of tags in the new tag dir

        status  = svn.cp(svn_repo+"/branches/"+branch, svn_repo+"/tags/"+newtagdir+"/"+newtag, "--no-auth-cache", "--non-interactive", "--username="+username, "--password="+passwd, "-m"+message)
        alltags = svn.ls(svn_repo+"/tags/"+newtagdir, "--no-auth-cache", "--non-interactive", "--username="+username, "--password="+passwd)
        return (status, alltags)
