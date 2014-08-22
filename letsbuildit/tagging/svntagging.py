from sh import svn
from tagging import models
from datetime import datetime

def createtagdir(newtagdir, message, comptype):
	vcs      = models.vc_credentials.objects.filter(version_control="svn").values()
	username = vcs[0]['userid']
	passwd   = vcs[0]['password']
	if comp_type == "non-shared":
		comp = models.components.objects.filter(component_name="SVN", version_control="svn").values()
	elif comp_type == "shared":
		comp = models.components.objects.filter(component_name="SVN2", version_control="svn").values()
	else:
		comp = models.components.objects.filter(component_name="SVN", version_control="svn").values()

	svn_repo = comp[0]['repo_path']
	status = svn.mkdir(svn_repo,"--no-auth-cache", "--non-interactive", "--username="+username, "--password="+passwd, "--parents" ,"-m"+message)	

	#Save this tagdir as latest tag
	if status == "":
		latesttag = newtagdir
		when = datetime.now()
		ctrl = models.tag_history(component_name=comptype, tag=latesttag, datetime=when, latest_tag=True)
		ctrl.save()
	return status

def createtag(newtag,newtagdir, message, comp_type):
	
	vcs      = models.vc_credentials.objects.filter(version_control="svn").values()
        username = vcs[0]['userid']
        passwd   = vcs[0]['password']

        if comp_type == "non-shared":
                comp = models.components.objects.filter(component_name="SVN", version_control="svn").values()
        elif comp_type == "shared":
                comp = models.components.objects.filter(component_name="SVN2", version_control="svn").values()
        else:
                comp = models.components.objects.filter(component_name="SVN", version_control="svn").values()

        svn_repo = comp[0]['repo_path']
        branch   = comp[0]['repo_path']
	# Create tag and get the list of tags in the new tag dir

	status  = svn.cp(svn_repo+"/branches/"+branch,svn_repo+"/tags/"+newtagdir+"/"+newtag, "--no-auth-cache", "--non-interactive", "--username="+username, "--password="+passwd, "-m"+message)
	alltags = svn.ls(svn_repo+"/tags/"+newtagdir, "--no-auth-cache", "--non-interactive", "--username="+username, "--password="+password)
	return (status, alltags)

