from django.contrib import admin
from tagging.models import vc_credentials, components,tag_history

# Register your models here.
admin.site.register(vc_credentials)
admin.site.register(components)
admin.site.register(tag_history)
