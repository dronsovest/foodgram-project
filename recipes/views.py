from django.shortcuts import render

from . import models


def index(request):
    latest = Recipe.objects.order_by("-pub_date")[:6]
    return render(request, "templates.index.html", latest)
