from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Favorites
from recipes.models import Recipe, Tag

import json


User = get_user_model()


@login_required
def favorite_list(request):
    recipes = Recipe.objects.filter(recipe_fav__user=request.user)
    recipes_tags = []
    is_favorites = True
    for recipe in recipes:
        tags = list(Tag.objects.filter(tag__recipe=recipe))
        recipes_tags.append((recipe, tags, is_favorites))
    paginator = Paginator(recipes_tags, 3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    title = "Избранное"
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "title": title
    })

@login_required
def favorites_add(request):
    request_body = json.loads(request.body)
    recipe_id = get_object_or_404(Recipe, id=int(request_body['id']))
    user_id = request.user
    Favorites.objects.get_or_create(user=user_id, recipe=recipe_id)
    return JsonResponse({"success": True})

@login_required
def favorites_del(request, id):
    favorites_recipe = get_object_or_404(Favorites, recipe=id, user=request.user)
    favorites_recipe.delete()
    return JsonResponse({"success": True})
