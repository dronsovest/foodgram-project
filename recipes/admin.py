from django.contrib import admin

from .models import Recipe, Ingredient, Tag, RecipeIngredients, TagsRecipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "pub_date", "author")
    search_fields = ("title", "author")
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "unit")
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    empty_value_display = "-пусто-"


class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "ingredient", "volume")
    list_filter = ("recipe",)
    empty_value_display = "-пусто-"


class TagsRecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "tag")
    list_filter = ("recipe",)
    empty_value_display = "-пусто-"


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(TagsRecipe, TagsRecipeAdmin)
