from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Recipe, Tag, Ingredient, RecipeIngredients
from .forms import RecipeForm
from favorites.models import Favorites


User = get_user_model()


def index(request):
    recipes = Recipe.objects.all()
    recipes_tags = []
    is_favorites = False
    for recipe in recipes:
        tags = list(Tag.objects.filter(tag__recipe=recipe))
        if request.user.is_authenticated:
            is_favorites = Favorites.objects.filter(
                recipe=recipe,
                user=request.user
            ).exists()
        recipes_tags.append((recipe, tags, is_favorites))
        paginator = Paginator(recipes_tags, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    title = "Рецепты"
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "title": title,
    })


def user_recipes(request, username):
    recipes = Recipe.objects.filter(author__username=username)
    recipes_tags = []
    is_favorites = False
    for recipe in recipes:
        tags = list(Tag.objects.filter(tag__recipe=recipe))
        if request.user.is_authenticated:
            is_favorites = Favorites.objects.filter(
                recipe=recipe,
                user=request.user
            ).exists()
        recipes_tags.append((recipe, tags, is_favorites))
        paginator = Paginator(recipes_tags, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    title = username
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        "title": title,
    })


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = Ingredient.objects.filter(ingredient__recipe=recipe)
    tags = list(Tag.objects.filter(tag__recipe=recipe))
    ing_vol = []
    is_favorites = False
    if request.user.is_authenticated:
        is_favorites = Favorites.objects.filter(recipe=recipe, user=request.user).exists()
    for ingredient in ingredients:
        volume = get_object_or_404(RecipeIngredients, ingredient=ingredient)
        ing_vol.append((ingredient, volume.volume))
    return render(request, "recipe.html", {
        "recipe": recipe,
        "ing_vol": ing_vol,
        "tags": tags,
        "is_favorites": is_favorites
    })


@login_required
def recipe_add(request):
    form = RecipeForm()
    edit = False
    title = "Создание рецепта"
    if not request.method == "POST":
        return render(request, "new.html", {
            "form": form,
            "edit": edit,
            "title": title,
        })
    form = RecipeForm(request.POST, files=request.FILES)
    if not form.is_valid():
        return render(request, "new.html", {
            "form": form,
            "edit": edit,
            "title": title,
        })
    recipe_get = form.save(commit=False)
    recipe_get.author = request.user
    recipe_get.save()
    return redirect("/")


@login_required
def recipe_edit(request, slug):
    pass


@login_required
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect("recipe", slug=slug)
    recipe.delete()
    return redirect("index")
