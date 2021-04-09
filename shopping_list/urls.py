from django.urls import path

from . import views


urlpatterns = [
    path("", views.shopping_list, name="shopping_list"),
    path("add/", views.shopping_list_add, name="shopping_list_add"),
    path("delete/<int:id>/", views.shopping_list_delete, name="shopping_list_delete"),
    path("download/", views.shopping_list_download, name="download")
]
