from django.db import models
from django.contrib.auth import get_user_model
from recipes.models import Recipe


User = get_user_model()


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_fav",
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_fav",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "recipe")
