from django.db import models

# Create your models here.

class vc_credentials(models.Model):
        VERSION           = (
               (u'svn',u'Subversion'),
               (u'git',u'Git'),
        )
        version_control   = models.CharField(max_length=3, choices=VERSION,primary_key=True)
        userid            = models.CharField("Username",max_length=20)
        password          = models.CharField("Password",max_length=20)

        def __unicode__(self):
		return self.version_control

class components(models.Model):
	component_name  = models.CharField("Component's Name",max_length=50,primary_key=True)
	component_type  = models.CharField("Component's Type",max_length=20)
        version_control = models.ForeignKey(vc_credentials)
        repo_path       = models.URLField("URL for git/svn")
        branch          = models.CharField("Branch",max_length=20)

	def __unicode__(self):
		return self.component_type

class tag_history(models.Model):
	component_name    = models.ForeignKey(components,primary_key=True)
        tag               = models.CharField(max_length=30)
        datetime          = models.DateField("When")
        latest_tag        = models.BooleanField()	

	def __unicode__(self):
		return u'%s %s' % (self.component_name, self.latest_tag)
