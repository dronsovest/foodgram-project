import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from .models import ShoppingList
from recipes.models import Recipe, RecipeIngredient, Ingredient
from recipes.utils import purchase_counter


@login_required
def shopping_list(request):
    recipes = Recipe.objects.filter(recipe_shl__user=request.user)
    title = "Список покупок"
    purchase_count = purchase_counter(request)
    return render(request, "shop-list.html", {
        "recipes": recipes,
        "title": title,
        "purchase_count": purchase_count,
    })


@login_required
def shopping_list_add(request):
    request_body = json.loads(request.body)
    recipe_id = get_object_or_404(Recipe, id=int(request_body.get('id')))
    user_id = request.user
    ShoppingList.objects.get_or_create(user=user_id, recipe=recipe_id)
    return JsonResponse({"success": True})


@login_required
def shopping_list_delete(request, id):
    recipe = get_object_or_404(ShoppingList, recipe=id, user=request.user)
    recipe.delete()
    if request.GET.get("reboot"):
        return redirect("shopping_list")
    return JsonResponse({"success": True})


def shopping_list_download(request):
    purchase_ingreditnts = RecipeIngredient.objects.filter(
        recipe__recipe_shl__user=request.user
    )
    precontent = {}
    for item in purchase_ingreditnts:
        ingredient = get_object_or_404(
            Ingredient,
            title=item.ingredient.title
        )
        if item.ingredient.title in precontent:
            precontent[item.ingredient.title][1] += item.volume
        else:
            precontent[item.ingredient.title] = [ingredient.unit, item.volume]
    content = ""
    for key, value in precontent.items():
        content += "{} ({}) - {}\n".format(key, value[0], value[1])
    filename = "purchase.txt"
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename
    )
    return response
