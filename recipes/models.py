from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model


User = get_user_model()


class Recipe(models.Model):
    title = models.CharField(
        max_length=60,
        db_index=True,
        verbose_name="Название рецепта"
        )
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор"
    )
    description = models.TextField()
    image = models.ImageField(
        upload_to="recipes/",
        null=True,
        verbose_name="Изображение"
    )
    cooking_time = models.PositiveIntegerField(verbose_name="Время приготовления")
    pub_date = models.DateTimeField(auto_now_add=True,
        verbose_name="Опубликовано"
    )

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return self.title


class TagsRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        related_name="tags",
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_tags",
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tag", "recipe"],
                name="unique_tag"
            )
        ]


class Ingredient(models.Model):
    title = models.CharField(max_length=60,
        db_index=True,
        verbose_name="Ингредиент"
    )
    unit = models.CharField(max_length=20, verbose_name="Единицы измерения")

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_ingredients",
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name="ingredients",
        on_delete=models.CASCADE
    )
    volume = models.FloatField(blank=True,
        null=True,
        verbose_name="Количество"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_ingredient"
            )
        ]
