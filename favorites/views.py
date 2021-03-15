from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def favorites_list(request):
    pass

@login_required
def favorites_add(request, recipe_slug):
    pass

@login_required
def favorites_del(request, recipe_slug):
    pass
