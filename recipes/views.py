import json

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .models import Recipe, Tag, Ingredient, RecipeIngredients, TagsRecipe
from .forms import RecipeForm
from favorites.models import Favorites
from follows.models import Follow
from shopping_list.models import ShoppingList


User = get_user_model()


def slugerfield(title):
    index = 1
    slug = title + str(index)
    while Recipe.objects.filter(slug=slug).exists():
        index += 1
        slug = title + str(index)
    return slug


def index(request):
    recipes = Recipe.objects.all()
    recipes_tags = []
    is_favorites = False
    is_purchase = False
    purchase_count = 0
    if request.user.is_authenticated:
        purchase_count = ShoppingList.objects.filter(user=request.user).count()
    for recipe in recipes:
        tags = list(Tag.objects.filter(tag__recipe=recipe))
        if request.user.is_authenticated:
            is_favorites = Favorites.objects.filter(
                recipe=recipe,
                user=request.user
            ).exists()
            is_purchase = ShoppingList.objects.filter(
                recipe=recipe,
                user=request.user
            ).exists()
        recipes_tags.append((recipe, tags, is_favorites, is_purchase))
        paginator = Paginator(recipes_tags, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    title = "Рецепты"
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "title": title,
        "purchase_count": purchase_count,
    })


def user_recipes(request, username):
    recipes = Recipe.objects.filter(author__username=username)
    recipes_tags = []
    is_favorites = False
    is_follow = False
    is_purchase = False
    purchase_count = 0
    if request.user.is_authenticated:
        purchase_count = ShoppingList.objects.filter(user=request.user).count()
        is_follow = Follow.objects.filter(
            author=get_object_or_404(User, username=username),
            user=request.user
        ).exists()
    for recipe in recipes:
        tags = list(Tag.objects.filter(tag__recipe=recipe))
        if request.user.is_authenticated:
            is_favorites = Favorites.objects.filter(
                recipe=recipe,
                user=request.user
            ).exists()
            is_purchase = ShoppingList.objects.filter(
                recipe=recipe,
                user=request.user
            ).exists()
        recipes_tags.append((recipe, tags, is_favorites, is_purchase))
        paginator = Paginator(recipes_tags, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    title = username
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "title": title,
        "is_follow": is_follow,
        "purchase_count": purchase_count,
    })


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = Ingredient.objects.filter(ingredient__recipe=recipe)
    tags = list(Tag.objects.filter(tag__recipe=recipe))
    ing_vol = []
    is_favorites = False
    is_purchase = False
    purchase_count = 0
    is_follow = False
    if request.user.is_authenticated:
        is_favorites = Favorites.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists()
        purchase_count = ShoppingList.objects.filter(user=request.user).count()
        is_follow = Follow.objects.filter(
            author=get_object_or_404(User, username=recipe.author.username),
            user=request.user
        ).exists()
        is_purchase = ShoppingList.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists()
    for ingredient in ingredients:
        volume = get_object_or_404(
            RecipeIngredients,
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
    form = RecipeForm()
    title = "Новый рецепт"
    purchase_count = ShoppingList.objects.filter(user=request.user).count()
    if not request.method == "POST":
        return render(request, "new.html", {
            "form": form,
            "title": title,
            "purchase_count": purchase_count,
        })
    form = RecipeForm(request.POST, files=request.FILES)
    if not form.is_valid():
        return render(request, "new.html", {
            "form": form,
            "title": title,
            "purchase_count": purchase_count,
        })
    recipe_get = form.save(commit=False)
    recipe_get.author = request.user
    recipe_get.slug = slugerfield(recipe_get.title)
    recipe_get.save()
    # Добавляем тэги и ингредиенты
    query_dict = request.POST.dict()
    for key, value in query_dict.items():
        if key == "breakfast" or key == "lunch" or key == "dinner":
            TagsRecipe.objects.create(
                tag=Tag.objects.get(title=key),
                recipe=Recipe.objects.get(slug=recipe_get.slug)
                )
        elif "nameIngredient" in key:
            key_value = "valueIngredient_" + key[15:]
            RecipeIngredients.objects.create(
                recipe=Recipe.objects.get(slug=recipe_get.slug),
                ingredient=Ingredient.objects.get(title=value),
                volume=query_dict[key_value]
            )
    return redirect("/")


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
        purchase_count = ShoppingList.objects.filter(user=request.user).count()
        tags = list(Tag.objects.filter(tag__recipe=recipe))
        ingredients = Ingredient.objects.filter(ingredient__recipe=recipe)
        ing_vol = []
        id_count = 1
        for ingredient in ingredients:
            volume = get_object_or_404(
                RecipeIngredients,
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
    recipe_get = form.save(commit=False)
    recipe_get.author = request.user
    recipe_get.slug = slug
    recipe_get.save()
    # Удаляем теги и рецепты для ингредиента
    TagsRecipe.objects.filter(recipe=recipe).delete()
    RecipeIngredients.objects.filter(recipe=recipe).delete()
    # Добавляем их заново из формы
    query_dict = request.POST.dict()
    for key, value in query_dict.items():
        if key == "breakfast" or key == "lunch" or key == "dinner":
            TagsRecipe.objects.create(
                tag=Tag.objects.get(title=key),
                recipe=Recipe.objects.get(slug=recipe_get.slug)
                )
        elif "nameIngredient" in key:
            key_value = "valueIngredient_" + key[15:]
            RecipeIngredients.objects.create(
                recipe=Recipe.objects.get(slug=recipe_get.slug),
                ingredient=Ingredient.objects.get(title=value),
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
