from django import forms

from .models import Recipe, Tag, TagsRecipe, Ingredient
from .utils import slugerfield


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        max_length=60,
        widget= forms.TextInput(attrs={"class":"form__input"})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "tags__checkbox"}),
        to_field_name="title",
        required=False
    )
    cooking_time = forms.IntegerField(
        max_value=500,
        widget=forms.NumberInput(attrs={"class":"form__input"})
    )
    ingredients = forms.CharField(
        max_length=60,
        required=False,
        widget= forms.TextInput(attrs={"class":"form__input"})
    )
    description = forms.CharField(
        max_length=20000,
        widget= forms.Textarea(attrs={"class":"form__textarea", "rows":"8"})
    )
    class Meta:
        model = Recipe
        fields = (
            "title",
            "tags",
            "cooking_time",
            "ingredients",
            "description",
            "image",
        )

    def clean_ingredients(self):
        query_dict =self.data.dict()
        ingredients_clean = []
        for key, value in query_dict.items(): 
            if "nameIngredient" in key:
                volume = "valueIngredient_" + key[15:]
                if int(query_dict[volume]) <= 0:
                    raise forms.ValidationError('Количество ингредиентов '
                                                'должно быть больше нуля')
                elif value in ingredients_clean:
                    raise forms.ValidationError('Один из ингредиентов был '
                                                'добавлен больше одного раза')
                elif not Ingredient.objects.filter(title=value).exists():
                    raise forms.ValidationError('Выберите ингредиент из '
                                                'выпадающего списка')
                else:
                    ingredients_clean.append(value)
        if len(ingredients_clean) == 0:
            raise forms.ValidationError('Добавьте ингредиент')
        return ingredients_clean

    def clean_tags(self):
        data = self.cleaned_data['tags']
        if len(data) == 0:
            raise forms.ValidationError('Добавьте тег')
        return data

    def save_recipe(self, request):
        recipe_get = self.save(commit=False)
        recipe_get.author = request.user
        recipe_get.slug = slugerfield(recipe_get.title)
        recipe_get.save()
        return recipe_get
