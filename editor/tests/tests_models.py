from django.test import TestCase

from editor.models import Topic, Newspaper, Redactor


class ModelsTests(TestCase):

    def test_topic_str(self) -> None:
        name = "IT"
        topic = Topic.objects.create(name=name)
        self.assertEqual(str(topic), name)


    def test_newspaper_str(self) -> None:
        topics = Topic.objects.bulk_create(
            (Topic(name="IT"), Topic(name="Politics"))
        )
        newspaper = Newspaper.objects.create(title="About Django")
        newspaper.topics.set(topics)

        self.assertEqual(
            str(newspaper),
            f"{newspaper.title} "
            f"(date: {newspaper.published_date} "
            f"topics: {", ".join(
                str(topic) for topic in newspaper.topics.all()
            )})"
        )
