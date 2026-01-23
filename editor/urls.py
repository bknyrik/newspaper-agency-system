from django.urls import path

from editor.views import (
    IndexView,
    TopicListView,
    TopicCreateView,
    TopicUpdateView,
)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
    path(
        "topics/<int:pk>/update/",
        TopicUpdateView.as_view(),
        name="topic-update"
    ),
]

app_name = "editor"
