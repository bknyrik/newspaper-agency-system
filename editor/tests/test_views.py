from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


TOPIC_URL = reverse("editor:topic-list")


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
