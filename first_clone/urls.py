"""first_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from first_apps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.IndexView.as_view(),name='index'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('new_post/',views.NewPostView.as_view(), name='new_post'),
    path('draft/',views.DraftListView.as_view(),name='draft_list'),
    path('draft/<int:pk>/',views.DraftDetailView.as_view(),name='draft_detail'),
    path('draft/<int:pk>/edit/',views.DraftUpdateView.as_view(),name='draft_edit'),
    path('draft/<int:pk>/delete/',views.DraftDeleteView.as_view(),name='draft_delete'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('post/<int:pk>/edit/',views.PostUpdateView.as_view(),name='post_edit'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name='post_delete'),
    path('draft/publish/',views.Publish.as_view(),name='publish'),
    path('new_comment/<int:pk>/',views.NewCommentView.as_view(), name='new_comment'),
    path('about/',views.AboutView.as_view(),name='about')
]
