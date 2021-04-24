import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Favorite
from recipes.models import Recipe, Tag
from shopping_list.models import ShoppingList


User = get_user_model()


@login_required
def favorite_list(request):
    recipes = Recipe.objects.filter(recipe_fav__user=request.user)
    recipes_tags = []
    is_favorites = True
    is_purchase = False
    purchase_count = ShoppingList.objects.filter(user=request.user).count()
    for recipe in recipes:
        tags = list(Tag.objects.filter(tags__recipe=recipe))
        is_purchase = ShoppingList.objects.filter(
                recipe=recipe,
                user=request.user
            ).exists()
        recipes_tags.append((recipe, tags, is_favorites, is_purchase))
    paginator = Paginator(recipes_tags, 3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    title = "Избранное"
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "title": title,
        "purchase_count": purchase_count,
    })


@login_required
def favorites_add(request):
    request_body = json.loads(request.body)
    if not request_body['id']:
        return JsonResponse({"success": False})
    recipe_id = get_object_or_404(Recipe, id=int(request_body['id']))
    user_id = request.user
    Favorite.objects.get_or_create(user=user_id, recipe=recipe_id)
    return JsonResponse({"success": True})


@login_required
def favorites_del(request, id):
    favorites_recipe = get_object_or_404(
        Favorite,
        recipe=id,
        user=request.user
    )
    favorites_recipe.delete()
    return JsonResponse({"success": True})
