from django.contrib import admin

from .models import ShoppingList


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "user")
    list_filter = ("recipe", "user")
    empty_value_display = "-пусто-"


admin.site.register(ShoppingList, ShoppingListAdmin)
