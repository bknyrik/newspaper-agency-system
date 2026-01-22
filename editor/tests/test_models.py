from django.test import TestCase
from django.contrib.auth import get_user_model

from editor.models import Topic, Newspaper, Redactor


class ModelTests(TestCase):

    def test_topic_str(self) -> None:
        name = "Test topic"
        topic = Topic.objects.create(name=name)
        self.assertEqual(str(topic), name)

    def test_newspaper_str(self) -> None:
        topics = Topic.objects.bulk_create(
            (
                Topic(name="Test topic"),
                Topic(name="Test topic 2")
            )
        )
        newspaper = Newspaper.objects.create(
            title="Test title"
        )
        newspaper.topics.set(topics)
        self.assertEqual(
            str(newspaper),
            f"{newspaper.title} "
            f"(date: {newspaper.published_date} "
            f"topics: {topics[0]}, {topics[1]})"
        )

    def test_redactor_str(self) -> None:
        redactor = get_user_model().objects.create(
            username="Test username",
            first_name="Test first",
            last_name="Test last"
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username}: ({redactor.get_full_name()})"
        )
