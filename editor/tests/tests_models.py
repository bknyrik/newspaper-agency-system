from django.test import TestCase

from editor.models import Topic, Newspaper, Redactor


class ModelsTests(TestCase):

    def test_topic_str(self) -> None:
        name = "IT"
        topic = Topic.objects.create(name=name)
        self.assertEqual(str(topic), name)
