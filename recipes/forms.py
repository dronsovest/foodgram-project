from .models import Recipe
from django.forms import ModelForm


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"
