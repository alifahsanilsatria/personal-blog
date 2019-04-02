from django import forms
from first_apps.models import Post,Comment,Draft
from django.forms import ModelForm
from django.db import models
from mediumeditor.widgets import MediumEditorTextarea

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class NewPostForm(ModelForm):
	class Meta:
		model = Draft
		fields = ['author','title','text']
		widgets = {
			'text' : MediumEditorTextarea(),
		}

class PublishForm(forms.Form):
	pk = forms.IntegerField(widget=forms.HiddenInput())
