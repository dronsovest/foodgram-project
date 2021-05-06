import json
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .models import Recipe, Tag, Ingredient, RecipeIngredient, TagsRecipe
from .forms import RecipeForm
from .utils import slugerfield, get_pagination, get_recipes
from .utils import purchase_counter, get_is_follow
from favorites.models import Favorite
from follows.models import Follow
from shopping_list.models import ShoppingList


User = get_user_model()


def index(request):
    recipes = get_recipes(request)
    all_tags = Tag.objects.all()
    recipes_tags = []
    purchase_count = purchase_counter(request)
    paginator = get_pagination(request, recipes, recipes_tags)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    title = "Рецепты"
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "title": title,
        "purchase_count": purchase_count,
        "all_tags": all_tags,
    })


def user_recipes(request, username):
    recipes = get_recipes(request)
    all_tags = Tag.objects.all()
    recipes = recipes.filter(author__username=username)
    recipes_tags = []
    author=get_object_or_404(User, username=username)
    is_follow = get_is_follow(request, author)
    purchase_count = purchase_counter(request)
    paginator = get_pagination(request, recipes, recipes_tags)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    title = username
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "title": title,
        "is_follow": is_follow,
        "purchase_count": purchase_count,
        "all_tags": all_tags,
    })


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = Ingredient.objects.filter(ingredients__recipe=recipe)
    tags = list(Tag.objects.filter(tags__recipe=recipe))
    ing_vol = []
    is_favorites = False
    is_purchase = False
    purchase_count = purchase_counter(request)
    is_follow = get_is_follow(request, recipe.author)
    if request.user.is_authenticated:
        is_favorites = Favorite.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists()
        is_purchase = ShoppingList.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists()
    for ingredient in ingredients:
        volume = get_object_or_404(
            RecipeIngredient,
            ingredient=ingredient,
            recipe=recipe
        )
        ing_vol.append((ingredient, volume.volume))
    return render(request, "recipe.html", {
        "recipe": recipe,
        "ing_vol": ing_vol,
        "tags": tags,
        "is_favorites": is_favorites,
        "is_follow": is_follow,
        "is_purchase": is_purchase,
        "purchase_count": purchase_count,
    })


@login_required
def recipe_add(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    purchase_count = purchase_counter(request)
    if form.is_valid():
        ingredients = form.cleaned_data['ingredients']
        recipe_get = form.save()
        form.cleaned_data['ingredients'] = []
        Ingredient.objects.bulk_create(
            get_ingredients_from_form(ingredients, recipe))
        # Добавляем тэги 
        query_dict = request.POST.dict() 
        for key, value in query_dict.items(): 
            if key in ["breakfast", "lunch", "dinner"]: 
                TagsRecipe.objects.create( 
                    tag = get_object_or_404(title=key), 
                    recipe = get_object_or_404(slug=recipe_get.slug) 
                    ) 
        return redirect("index")
    context = {"title": "Новый рецепт",
               "form": form,
               "purchase_count": purchase_count,
               }
    return render(request, "new.html", context)


@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect("recipe", slug=slug)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe)
    if not form.is_valid():
        title = "Редактирование рецепта"
        purchase_count = purchase_counter(request)
        tags = list(Tag.objects.filter(tags__recipe=recipe))
        ingredients = Ingredient.objects.filter(ingredients__recipe=recipe)
        ing_vol = []
        id_count = 1
        for ingredient in ingredients:
            volume = get_object_or_404(
                RecipeIngredient,
                ingredient=ingredient,
                recipe=recipe
            )
            ing_id = "ing_" + str(id_count)
            ing_name_id = "Ingredient_" + str(id_count)
            ing_vol.append((ingredient, volume.volume, ing_id, ing_name_id))
            id_count += 1
        return render(request, "new.html", {
            "form": form,
            "title": title,
            "purchase_count": purchase_count,
            "recipe": recipe,
            "tags": tags,
            "ing_vol": ing_vol,
        })
    recipe_get = form.save()
    # Удаляем теги и рецепты для ингредиента
    TagsRecipe.objects.filter(recipe=recipe).delete()
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    # Добавляем их заново из формы
    query_dict = request.POST.dict()
    for key, value in query_dict.items():
        if key in ["breakfast", "lunch", "dinner"]:
            TagsRecipe.objects.create(
                tag = get_object_or_404(title=key),
                recipe = get_object_or_404(slug=recipe_get.slug)
                )
        elif "nameIngredient" in key:
            key_value = "valueIngredient_" + key[15:]
            RecipeIngredient.objects.create(
                recipe=get_object_or_404(slug=recipe_get.slug),
                ingredient=get_object_or_404(title=value),
                volume=query_dict[key_value]
            )
    return redirect("recipe", slug=slug)


@login_required
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect("recipe", slug=slug)
    recipe.delete()
    return redirect("index")


def ingredients_query(request):
    query = request.GET["query"]
    ingredients = Ingredient.objects.filter(title__contains=query)
    response = []
    for ingredient in ingredients:
        response.append({
            "title": ingredient.title,
            "dimension": ingredient.unit
        })
    return JsonResponse(response, safe=False)
