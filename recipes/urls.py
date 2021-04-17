from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<slug>/", views.recipe_view, name="recipe"),
    path("recipe-add/", views.recipe_add, name="recipe_add"),
    path("recipe-edit/<slug>/", views.recipe_edit, name="recipe_edit"), 
    path("recipe-delete/<slug>/", views.recipe_delete, name="recipe_delete"),
    path("users/<username>", views.user_recipes , name="user_recipes"),
    path("ingredients", views.ingredients_query, name="ingredients_query"),
]