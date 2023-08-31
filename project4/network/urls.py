
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    
    # API routes
    path("follow/<str:username>", views.follow, name="follow"),
    path("create-post", views.create_post, name="create-post"),
    path("edit-post", views.edit_post, name="edit-post"),
    path("like-post", views.like_post, name="like-post"),
]
