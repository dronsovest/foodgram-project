from .models import Recipe, Tag, TagsRecipe
from django import forms


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tags__checkbox'}),
        to_field_name='slug',
        required=False
    )
    
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'cooking_time', 'description',
                  'image')
        def clean_ingredients(self):
            ingredient_names = self.data.getlist('nameIngredient')
            ingredient_units = self.data.getlist('unitsIngredient')
            ingredient_amounts = self.data.getlist('valueIngredient')
            ingredients_clean = []
            for ingredient in zip(ingredient_names, ingredient_units,
                                  ingredient_amounts):
                if int(ingredient[2]) < 0:
                    raise forms.ValidationError('Количество ингредиентов должно '
                                                'быть больше нуля')
                else:
                    ingredients_clean.append({'title': ingredient[0],
                                          'unit': ingredient[1],
                                          'amount': ingredient[2]})
            if len(ingredients_clean) == 0:
                raise forms.ValidationError('Добавьте ингредиент')
            return ingredients_clean
