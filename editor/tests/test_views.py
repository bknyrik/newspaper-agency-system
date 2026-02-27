from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from editor.models import Topic


TOPIC_URL = reverse("editor:topic-list")
NEWSPAPER_LIST_URL = reverse("editor:newspaper-list")
NEWSPAPER_DETAIL_URL = reverse("editor:newspaper-detail", kwargs={"pk": 1})


class PublicTopicTests(TestCase):

    def test_login_required(self) -> None:
        response = self.client.get(TOPIC_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTopicTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_topics(self) -> None:
        topics = Topic.objects.bulk_create(
            [
                Topic(name="Economics"),
                Topic(name="Nature")
            ]
        )
        response = self.client.get(TOPIC_URL)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(tuple(topics), tuple(response.context["topic_list"]))
        self.assertTemplateUsed(response, "editor/topic_list.html")

    def test_create_topic(self) -> None:
        self.client.post(
            reverse("editor:topic-create"),
            data={"name": "TEST"}
        )
        self.assertEqual(Topic.objects.get(pk=1).name, "TEST")

    def test_update_topic(self) -> None:
        Topic.objects.create(name="Politics")
        self.client.post(
            reverse("editor:topic-update", kwargs={"pk": 1}),
            data={"name": "IT"}
        )
        self.assertEqual(Topic.objects.get(pk=1).name, "IT")

    def test_delete_topic(self) -> None:
        Topic.objects.create(name="Sport")
        self.client.post(reverse("editor:topic-delete", kwargs={"pk": 1}))
        self.assertEqual(Topic.objects.count(), 0)


class PublicNewspaperTests(TestCase):

    def test_newspaper_list_login_required(self) -> None:
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_newspaper_detail_login_required(self) -> None:
        response = self.client.get(NEWSPAPER_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)
