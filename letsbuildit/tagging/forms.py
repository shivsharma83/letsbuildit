from django import forms
from django.forms.formsets import formset_factory

class Tagit(forms.Form):
	tag = forms.CharField()


TagitFormSet = formset_factory(Tagit,extra=2)

