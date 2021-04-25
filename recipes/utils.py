from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .models import Recipe, Tag
from favorites.models import Favorite
from shopping_list.models import ShoppingList
from follows.models import Follow


def slugerfield(title):
    index = 1
    slug = title + str(index)
    while Recipe.objects.filter(slug=slug).exists():
        index += 1
        slug = title + str(index)
    return slug


def get_pagination(request, recipes, recipes_tags):
    for recipe in recipes:
        tags = list(Tag.objects.filter(tags__recipe=recipe))
        if request.user.is_authenticated:
            is_favorites = Favorite.objects.filter(
                recipe=recipe,
                user=request.user
            ).exists()
            is_purchase = ShoppingList.objects.filter(
                recipe=recipe,
                user=request.user
            ).exists()
        recipes_tags.append((recipe, tags, is_favorites, is_purchase))
    paginator = Paginator(recipes_tags, settings.PAGE_SIZE)
    return paginator


def purchase_counter(request):
    if request.user.is_authenticated:
        return ShoppingList.objects.filter(user=request.user).count()
    return 0


def get_is_follow(request, author):
    if request.user.is_authenticated:
        return (Follow.objects.filter(
            author=author,
            user=request.user
        ).exists())
    return False
