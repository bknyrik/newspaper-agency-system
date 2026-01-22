from django.db import models
from django.db.models import constraints
from django.db.models import functions
from django.contrib.auth import settings
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

    def __str__(self) -> str:
        return f"{self.username} ({self.get_full_name()})"


class Newspaper(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topics = models.ManyToManyField(Topic, related_name="newspapers")
    publishers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="newspapers")

    class Meta:
        constraints = (
            constraints.UniqueConstraint(
                functions.Lower("title"),
                name="unique_lower_title"
            ),
        )

    def __str__(self) -> str:
        return (
            f"{self.title} "
            f"(date: {self.published_date} "
            f"topics: {", ".join(str(topic) for topic in self.topics.all())})"
        )
