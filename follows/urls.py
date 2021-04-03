from django.urls import path

from . import views


urlpatterns = [
    path("", views.follows_list, name="follows_list"),
    path("add/", views.follows_add, name="follows_add"),
    path("remove/<str:username>/", views.follows_remove, name="follow_remove"),
]
