import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Favorite
from recipes.models import Recipe, Tag
from shopping_list.models import ShoppingList
from recipes.utils import get_pagination, purchase_counter, get_recipes


User = get_user_model()


@login_required
def favorite_list(request):
    recipes = get_recipes(request).filter(recipe_fav__user=request.user)
    all_tags = Tag.objects.all()
    recipes_tags = []
    purchase_count = purchase_counter(request)
    paginator = get_pagination(request, recipes, recipes_tags)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    title = "Избранное"
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "title": title,
        "purchase_count": purchase_count,
        "all_tags": all_tags,
    })


@login_required
def favorites_add(request):
    request_body = json.loads(request.body)
    recipe_id = get_object_or_404(Recipe, id=int(request_body.get('id')))
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
