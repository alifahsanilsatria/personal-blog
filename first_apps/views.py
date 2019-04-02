from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView
from django.urls import reverse_lazy,reverse
from django.shortcuts import render
from first_apps.forms import LoginForm, NewPostForm, PublishForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from first_apps import models
from django.contrib.auth.models import User
from first_apps import models
from django import forms
from mediumeditor.widgets import MediumEditorTextarea
# Create your views here.

class IndexView(View):
	def get(self,request):
		post_list = models.Post.objects.all()
		if request.user.is_authenticated:
			username = request.user.username
			return render(request,'first_apps/index.html',
				{'username' : username, 
				'post_list' : post_list})
		else:
			return render(request,'first_apps/index.html',
				{'post_list' : post_list})

class LoginView(View):
	template_name = 'first_apps/login.html'
	def get(self,request):
		form = LoginForm()
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		username = request.POST['username']
		password = request.POST['password']

		#django's built-in authentication function:	
		user = authenticate(username=username, password=password)
		if user:
			login(request,user)
			return redirect('index')
		else:
			form = LoginForm()
			return render(request,self.template_name,{"form":form})

@method_decorator(login_required, name='get')
class LogoutView(View):
	def get(self,request):
		main_page = 'first_apps/index.html'
		
		#Log out the user
		logout(request)

		return redirect('index')

class NewPostView(View):
	def get(self,request):
		form = NewPostForm()
		username = request.user.username
		return render(request,'first_apps/new_post.html',{'form' : form, 'username' : username})

	def post(self,request):
		author = User.objects.get(pk=request.POST['author'])
		title = request.POST['title']
		text = request.POST['text']

		new_draft = models.Draft(author=author, title=title, text=text)
		new_draft.save()
		return redirect('draft_detail', pk=new_draft.id)

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class DraftListView(ListView):
	model = models.Draft
	template_name = 'first_apps/draft_list.html'
	context_object_name ='draft_list'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['username'] = self.request.user.username
		return context

class DraftDetailView(DetailView):
	model = models.Draft
	template_name = 'first_apps/draft_detail.html'
	context_object_name = 'draft'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['username'] = self.request.user.username
		context['publish_form'] = PublishForm(
			initial={'pk' : context['draft'].id})	
		return context

class DraftUpdateView(UpdateView):
	model = models.Draft
	fields = ("author","title","text")
	template_name = 'first_apps/new_post.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['username'] = self.request.user.username
		context['form'].fields['text'].widget = MediumEditorTextarea()
		return context

class DraftDeleteView(DeleteView):
	model = models.Draft
	success_url = reverse_lazy('draft_list')
	template_name = 'first_apps/draft_detail.html'
	context_object_name = 'draft'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['username'] = self.request.user.username
		context['delete_click'] = True
		return context

class Publish(View):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self,request):
		draft = models.Draft.objects.get(pk=request.POST['pk'])
		author = draft.author
		title = draft.title
		text = draft.text

		published_post = models.Post(author=author, title=title, text=text)
		published_post.save()

		draft.delete()

		return redirect('post_detail',pk=published_post.id)

class PostDetailView(DetailView):
	model = models.Post
	template_name = 'first_apps/post_detail.html'
	context_object_name = 'post'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if(self.request.user.is_authenticated):
			context['username'] = self.request.user.username
		
		comment_list= models.Comment.objects.filter(related_post=self.kwargs['pk'])
		
		if(comment_list.exists()):
			context['comment_list'] = comment_list
		return context

class PostUpdateView(UpdateView):
	model = models.Post
	fields = ("author","title","text")
	template_name = 'first_apps/new_post.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['username'] = self.request.user.username
		context['form'].fields['text'].widget = MediumEditorTextarea()
		return context

class PostDeleteView(DeleteView):
	model = models.Post
	success_url = reverse_lazy('index')
	template_name = 'first_apps/post_detail.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['username'] = self.request.user.username
		context['delete_click'] = True
		return context

class NewCommentView(CreateView):
	model = models.Comment
	fields = ['related_post','author','text']
	template_name = 'first_apps/new_comment.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["username"] =  self.request.user.username
		context["form"].fields['related_post'].widget = forms.HiddenInput()
		context["form"].fields['related_post'].initial = models.Post.objects.get(pk=self.kwargs['pk'])
		return context

class AboutView(View):
	def get(self,request):
		return render(request,'first_apps/about.html')