from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from time import localtime, strftime
from mediumeditor.admin import MediumEditorAdmin

# Create your models here.
class Post(models.Model):
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length=50)
	text = models.TextField()
	publish_time = models.CharField(max_length=100, default=strftime("%d %B %Y, %H:%M %p",localtime()))

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk':self.id})

	def get_absolute_url_edit(self):
		return reverse('post_edit', kwargs={'pk':self.id})

	def get_absolute_url_delete(self):
		return reverse('post_delete',kwargs={'pk':self.id})

	def get_absolute_url_comment(self):
		return reverse('new_comment',kwargs={'pk':self.id})

class Comment(models.Model):
	related_post  = models.ForeignKey(Post, on_delete = models.CASCADE)
	author = models.CharField(max_length=30)
	text = 	models.TextField()
	publish_time = models.CharField(max_length=100, default=strftime("%d %B %Y, %H:%M %p",localtime()))

	def get_absolute_url(self):
		return reverse("post_detail", kwargs={"pk": self.related_post.id})
	
class Draft(models.Model):
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length=50)
	text = models.TextField()

	def get_absolute_url(self):
		return reverse('draft_detail', kwargs={'pk':self.id})

	def get_absolute_url_edit(self):
		return reverse('draft_edit', kwargs={'pk':self.id})

	def get_absolute_url_delete(self):
		return reverse('draft_delete',kwargs={'pk':self.id})
