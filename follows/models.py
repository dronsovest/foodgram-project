from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name="follower",
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "author")