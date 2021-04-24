from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model

from recipes.models import Recipe


User = get_user_model()


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_shl",
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_shl",
        on_delete=models.CASCADE
    )

    class Meta:
        UniqueConstraint(fields=["user", "recipe"], name="unique_purchase")
