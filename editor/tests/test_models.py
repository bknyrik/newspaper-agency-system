from django.test import TestCase

from editor.models import Topic


class ModelTests(TestCase):

    def test_topic_str(self) -> None:
        name = "Test topic"
        topic = Topic.objects.create(name=name)
        self.assertEqual(str(topic), name)
