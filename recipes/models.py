from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Recipe(models.Model):
    name = models.CharField(max_length=60, blank=False)
    slug = models.SlugField(unique=True, blank=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        blank=False,
    )
    description = models.TextField(blank=False, )
    image = models.ImageField(
        upload_to="recipes/",
        null=True,
        verbose_name="Изображение",
        blank=False,
    )
    cooking_time = models.DurationField(blank=False, )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        blank=False,
    )
