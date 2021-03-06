from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Recipe(models.Model):
    title = models.CharField(max_length=60, db_index=True)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    description = models.TextField()
    image = models.ImageField(
        upload_to="recipes/",
        null=True,
        verbose_name="Изображение"
    )
    cooking_time = models.DurationField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-pub_date",)


class Tag(models.Model):
    title = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return self.title


class TagsRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        related_name="tag",
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_tag",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("tag", "recipe")


class Ingredient(models.Model):
    title = models.CharField(max_length=60, db_index=True)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_ing",
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name="ingredient",
        on_delete=models.CASCADE
    )
    volume = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ("recipe", "ingredient")
