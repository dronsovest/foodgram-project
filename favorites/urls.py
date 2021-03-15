from django.urls import path

from . import views


urlpatterns = [
    path("", views.favorites_list, name="favorites_list"),
    path("add/<recipe_slug>", views.favorites_add, name="favorites_add"),
    path("delete/<recipe_slug>", views.favorites_del, name="favorites_delete")
]
