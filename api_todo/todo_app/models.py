from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):

    user = user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    complete = models.BooleanField(
        default=False
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.description
