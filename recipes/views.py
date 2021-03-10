from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .models import Recipe, Tag, Ingredient, RecipeIngredients
from .forms import RecipeForm


def index(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
    })

def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = Ingredient.objects.filter(ingredient__recipe=recipe)
    tags = list(Tag.objects.filter(tag__recipe=recipe))
    ing_vol = []
    for ingredient in ingredients:
        volume = get_object_or_404(RecipeIngredients, ingredient=ingredient)
        ing_vol.append((ingredient, volume.volume))
    return render(request, "recipe.html", {
        "recipe": recipe,
        "ing_vol": ing_vol,
        "tags": tags
    })


def recipe_add(request):
    form = RecipeForm()
    edit = False
    if not request.method == "POST":
        return render(request, "new.html", {
            "form": form,
            "edit": edit,
        })
    form = RecipeForm(request.POST, files=request.FILES)
    if not form.is_valid():
        return render(request, "new.html", {
            "form": form,
            "edit": edit,
        })
    recipe_get = form.save(commit=False)
    recipe_get.author = request.user
    recipe_get.save()
    return redirect("/")

def recipe_edit(request, slug):
    pass

@login_required
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect("recipe", slug=slug)
    recipe.delete()
    return redirect("index")
