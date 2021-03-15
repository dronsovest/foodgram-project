from django.urls import path

from . import views


urlpatterns = [
    path("", views.follows_list, name="follows_list"),
]
