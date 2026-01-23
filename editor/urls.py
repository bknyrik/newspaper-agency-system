from django.urls import path

from editor.views import (
    IndexView,
    TopicListView,
)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
]

app_name = "editor"
