from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Favorites
from recipes.models import Recipe, Tag


User = get_user_model()


@login_required
def favorite_list(request):
    recipes = Recipe.objects.filter(recipe_fav__user=request.user)
    recipes_tags = []
    for recipe in recipes:
        tags = list(Tag.objects.filter(tag__recipe=recipe))
        recipes_tags.append((recipe, tags))
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
    print(request)

@login_required
def favorites_del(request, recipe_slug):
    pass
