
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>", views.profile, name="prof"),
    path("following", views.only_following, name="only_follows"),

    # API routes
    path("make-post", views.create_post, name="makepost"),
    path("follow", views.follow, name="to_follow"),
    path("like", views.to_like, name="like")
]
