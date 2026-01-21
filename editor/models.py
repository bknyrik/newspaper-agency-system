from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators


class Topic(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ("name", )

    def __str__(self) -> str:
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(
        null=True,
        blank=True,
        validators=(
            validators.MinValueValidator(limit_value=1),
        )
    )

    class Meta:
        verbose_name = "redactor"
