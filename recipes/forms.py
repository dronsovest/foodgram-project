from django import forms

from .models import Recipe, Tag, TagsRecipe


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        max_length=60,
        widget= forms.TextInput(attrs={"class":"form__input"})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tags__checkbox'}),
        to_field_name='title',
        required=False
    )
    cooking_time = forms.IntegerField(
        max_value=500,
        widget=forms.NumberInput(attrs={"class":"form__input"})
    )
    description = forms.CharField(
        max_length=20000,
        widget= forms.Textarea(attrs={"class":"form__textarea", "rows":"8"})
    )
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'cooking_time', 'description', 'image')

    def clean_ingredients(self):
        ingredient_names = self.data.getlist('nameIngredient')
        ingredient_units = self.data.getlist('unitsIngredient')
        ingredient_amounts = self.data.getlist('valueIngredient')
        ingredients_clean = []
        for title, unit, amount in zip(ingredient_names, ingredient_units,
                                       ingredient_amounts):
            if int(unit) < 0:
                raise forms.ValidationError('Количество ингредиентов '
                                            'должно быть больше нуля')
            else:
                ingredients_clean.append({
                    'title': title,
                    'unit': unit,
                    'amount': amount
                })
        if len(ingredients_clean) == 0:
            raise forms.ValidationError('Добавьте ингредиент')
        return ingredients_clean

    def clean_tags(self):
        data = self.cleaned_data['tags']
        if len(data) == 0:
            raise forms.ValidationError('Добавьте тег')
        return data

    def save(self):
        recipe_get = form.save(commit=False)
        recipe_get.author = request.user
        recipe_get.slug = slug
        recipe_get.save()
        return recipe_get
