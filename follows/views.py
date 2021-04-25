from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
import json

from .models import Follow
from .utils import format_counter
from recipes.models import Recipe
from shopping_list.models import ShoppingList
from recipes.utils import purchase_counter


User = get_user_model()


@login_required
def follows_list(request):
    title = "Мои подписки"
    purchase_count = purchase_counter(request)
    authors = User.objects.filter(following__user=request.user)
    authors_recipes = []
    for author in authors:
        recipes_count = Recipe.objects.filter(author=author).count()
        recipes = Recipe.objects.filter(author=author)[:3]
        authors_recipes.append((
            author,
            recipes,
            format_counter(recipes_count)
        ))
    paginator = Paginator(authors_recipes, 3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {
        "page": page,
        "paginator": paginator,
        "title": title,
        "purchase_count": purchase_count,
    })


@login_required
def follows_add(request):
    request_body = json.loads(request.body)
    author = get_object_or_404(User, username=request_body.get('id'))
    if request.user == author:
        return redirect("user_recipes", username=author.username)
    new_follow = Follow.objects.get_or_create(
        user=request.user,
        author=author
    )
    return JsonResponse({"success": True})


@login_required
def follows_remove(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return JsonResponse({"success": True})
