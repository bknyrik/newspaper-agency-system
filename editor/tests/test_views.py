from django.test import TestCase
from django.shortcuts import reverse


TOPIC_URL = reverse("editor:topic-list")


class PublicTopicTests(TestCase):

    def test_login_required(self) -> None:
        response = self.client.get(TOPIC_URL)
        self.assertNotEqual(response.status_code, 200)
