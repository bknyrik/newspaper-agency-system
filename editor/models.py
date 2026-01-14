from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import settings


class Topic(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ("name", )

    def __str__(self) -> str:
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topics = models.ManyToManyField(Topic, related_name="newspapers")
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="newspapers"
    )


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ("username", )
        verbose_name = "redactors"

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"
