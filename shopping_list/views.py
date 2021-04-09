from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from .models import ShoppingList
from recipes.models import Recipe, RecipeIngredients, Ingredient

import json


@login_required
def shopping_list(request):
    recipes = Recipe.objects.filter(recipe_shl__user=request.user)
    title = "Список покупок"
    purchase_count = ShoppingList.objects.filter(user=request.user).count()
    return render(request, "shop-list.html", {
        "recipes": recipes,
        "title": title,
        "purchase_count": purchase_count,
    })


@login_required
def shopping_list_add(request):
    request_body = json.loads(request.body)
    recipe_id = get_object_or_404(Recipe, id=int(request_body['id']))
    user_id = request.user
    ShoppingList.objects.get_or_create(user=user_id, recipe=recipe_id)
    return JsonResponse({"success": True})


@login_required
def shopping_list_delete(request, id):
    print(id, request.user)
    recipe = get_object_or_404(ShoppingList, recipe=id, user=request.user)
    recipe.delete()
    return JsonResponse({"success": True})
    

def shopping_list_download(request):
    purchase_ingreditnts = RecipeIngredients.objects.filter(
        recipe__recipe_shl__user=request.user
    )
    content = ""
    for item in purchase_ingreditnts:
        ingredient = Ingredient.objects.get(title=item.ingredient.title)
        content += "{} ({}) - {}\n".format(item.ingredient.title, ingredient.unit, item.volume)
    filename = "purchase.txt"
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
