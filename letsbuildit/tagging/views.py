from django.http import HttpResponse

# Create your views here.

def vcs(request):
	return HttpResponse("Hello, I will show available version controls here")
