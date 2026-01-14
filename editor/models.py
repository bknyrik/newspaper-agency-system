from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_data = models.DateField()
    topics = models.ManyToManyField(Topic, related_name="newspapers")
