from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from cat import views
from django.views.generic.base import RedirectView

from django.contrib.auth import views as auth

# from .views import ContactView
urlpatterns = [ 
    path('home/', views.HomeView.as_view()),
    path('about/', views.AboutView.as_view()),

    path('accounts/register/',views.registerPage,name="register"),
    path('profile/edit/<int:pk>', views.MyProfileUpdateView.as_view(success_url="/cat/home")),
    
    path('mypost/create/', views.MyPostCreate.as_view(success_url="/cat/mypost")),
    path('mypost/delete/<int:pk>', views.MyPostDeleteView.as_view(success_url="/cat/mypost")),
    path('mypost/', views.MyPostListView.as_view()),
    path('mypost/<int:pk>', views.MyPostDetailView.as_view()),

    path('mypost/<int:pk>/add-comment', views.add_comment, name='add-comment'),

    path('mypost/like/<int:pk>', views.like),
    path('mypost/unlike/<int:pk>', views.unlike),

    path('postcomment-delete/<int:pk>', views.PostCommentDeleteView.as_view(success_url="/cat/mypost/")),
    path('myprofile/', views.MyProfileListView.as_view()),
    path('myprofile/<int:pk>', views.MyProfileDetailView.as_view()),
    path('myprofile/follow/<int:pk>', views.follow),
    path('myprofile/unfollow/<int:pk>', views.unfollow),

    path('', RedirectView.as_view(url="home/")),  
   
]
       



