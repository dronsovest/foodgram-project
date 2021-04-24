from django.urls import path

from . import views


urlpatterns = [
    path('500/', views.server_error),
    path("", views.index, name="index"),
    path("recipe/<str:slug>/", views.recipe_view, name="recipe"),
    path("recipe-add/", views.recipe_add, name="recipe_add"),
    path("recipe-edit/<str:slug>/", views.recipe_edit, name="recipe_edit"),
    path("recipe-delete/<str:slug>/", views.recipe_delete, name="recipe_delete"),
    path("users/<str:username>/", views.user_recipes, name="user_recipes"),
    path("ingredients/", views.ingredients_query, name="ingredients_query"),
]
urlpatterns += [
    path('404/', views.page_not_found),
]
