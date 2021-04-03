from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Follow
from recipes.models import Recipe


User = get_user_model()


@login_required
def follows_list(request):
    title = "Мои подписки"
    authors = User.objects.filter(following__user=request.user)
    authors_recipes = []
    for author in authors:
        recipes_count = Recipe.objects.filter(author=author).count()
        recipes = Recipe.objects.filter(author=author)[:3]
        authors_recipes.append((author, recipes, recipes_count -3 ))
    paginator = Paginator(authors_recipes, 3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {
        "page": page,
        "paginator": paginator,
        "title": title
    })


def follows_add(request):
    pass


def follows_remove(request, username):
    pass
