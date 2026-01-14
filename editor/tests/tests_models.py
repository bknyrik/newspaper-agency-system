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

    def test_redactor_str(self) -> None:
        redactor = Redactor.objects.create(
            username="johndoe",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username} "
            f"({redactor.first_name} {redactor.last_name})"
        )

    def test_create_redactor_with_years_of_experience(self) -> None:
        data = {
            "username": "peterparker",
            "password": "a1b2c3d4",
            "years_of_experience": 20
        }
        redactor = Redactor.objects.create_user(**data)
        self.assertEqual(redactor.username, data["username"])
        self.assertTrue(redactor.check_password(data["password"]))
        self.assertEqual(
            redactor.years_of_experience,
            data["years_of_experience"]
        )
