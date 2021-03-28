from django.urls import path

from . import views


urlpatterns = [
    path("", views.favorite_list, name="favorites_list"),
    path("add/", views.favorites_add, name="favorites_add"),
    path("delete/<int:id>", views.favorites_del, name="favorites_delete")
]
