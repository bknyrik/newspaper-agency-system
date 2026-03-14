from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from editor.models import Topic, Newspaper, Redactor


TOPIC_LIST_URL = reverse("editor:topic-list")
NEWSPAPER_LIST_URL = reverse("editor:newspaper-list")
NEWSPAPER_DETAIL_URL = reverse("editor:newspaper-detail", kwargs={"pk": 1})
REDACTOR_LIST_URL = reverse("editor:redactor-list")
REDACTOR_DETAIL_URL = reverse("editor:redactor-detail", kwargs={"pk": 1})


class PublicTopicTests(TestCase):

    def test_login_required(self) -> None:
        response = self.client.get(TOPIC_LIST_URL)
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
        response = self.client.get(TOPIC_LIST_URL)
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
        new_name = "IT"
        politics = Topic.objects.create(name=new_name)
        self.client.post(
            reverse("editor:topic-update", kwargs={"pk": 1}),
            data={"name": "IT"}
        )
        self.assertEqual(politics.name, new_name)

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


class PrivateNewspaperTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345"
        )
        self.newspaper = Newspaper.objects.create(
            title="Test title",
            content="Test content"
        )
        self.topic = Topic.objects.create(name="TEST_TOPIC")
        self.newspaper.topics.set([self.topic])
        self.newspaper.publishers.set([self.user])
        self.client.force_login(self.user)

    def test_retrieve_newspapers(self) -> None:
        response = self.client.get(NEWSPAPER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            tuple(Newspaper.objects.all()),
            tuple(response.context["newspaper_list"])
        )
        self.assertTemplateUsed(response, "editor/newspaper_list.html")

    def test_get_newspaper(self) -> None:
        response = self.client.get(NEWSPAPER_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.newspaper.id, response.context["newspaper"].id)
        self.assertTemplateUsed(response, "editor/newspaper_detail.html")

    def test_delete_authenticated_redactor_from_newspaper(self) -> None:
        self.client.post(NEWSPAPER_DETAIL_URL)
        self.assertEqual(self.newspaper.publishers.count(), 0)

    def test_assign_authenticated_redactor_to_newspaper(self) -> None:
        user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testpassword12345"
        )
        self.client.force_login(user2)
        self.client.post(NEWSPAPER_DETAIL_URL)
        self.assertEqual(self.newspaper.publishers.count(), 2)

    def test_create_newspaper(self) -> None:
        data = {
            "title": "Test title 2",
            "content": "Test content 2",
            "topics": [self.topic.id],
            "publishers": [self.user.id]
        }
        self.client.post(
            path=reverse("editor:newspaper-create"),
            data=data
        )
        newspaper = Newspaper.objects.get(pk=2)
        self.assertEqual(newspaper.title, data["title"]),
        self.assertEqual(newspaper.content, data["content"]),
        self.assertEqual(
            newspaper.publishers.first().id,
            data["publishers"][0]
        )
        self.assertEqual(newspaper.topics.first().id, data["topics"][0])

    def test_update_newspaper(self) -> None:
        data = {
            "title": "Another title",
            "content": "Another content",
            "topics": [self.topic.id],
            "publishers": [self.user.id]
        }
        self.client.post(
            reverse("editor:newspaper-update", kwargs={"pk": self.newspaper.id}),
            data=data
        )
        newspaper = Newspaper.objects.get(pk=1)
        self.assertEqual(newspaper.title, data["title"])
        self.assertEqual(newspaper.content, data["content"])

    def test_delete_newspaper(self) -> None:
        self.client.post(
            reverse("editor:newspaper-delete", kwargs={"pk": 1})
        )
        self.assertEqual(Newspaper.objects.count(), 0)


class PublicRedactorTests(TestCase):

    def test_redactor_list_login_required(self) -> None:
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateRedactorTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass12345"
        )
        self.client.force_login(user=self.user)

    def test_retrieve_redactors(self) -> None:
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertEqual(
            tuple(Redactor.objects.all()),
            tuple(response.context["redactor_list"])
        )
        self.assertTemplateUsed(response, "editor/redactor_list.html")

    def test_get_redactor(self) -> None:
        response = self.client.get(
            reverse("editor:redactor-detail", kwargs={"pk": 1}),
        )
        self.assertEqual(
            self.user.username,
            response.context["redactor"].username
        )
        self.assertTrue(
            response.context["redactor"].check_password("testpass12345")
        )

    def test_create_redactor(self) -> None:
        data = {
            "username": "testuser2",
            "first_name": "test first name",
            "last_name": "test last name",
            "years_of_experience": 10,
            "email": "test@mail.com",
            "password1": "testpass1234",
            "password2": "testpass1234"
        }
        self.client.post(
            path=reverse("editor:redactor-create"),
            data=data
        )
        user = Redactor.objects.get(username=data["username"])

        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.years_of_experience, data["years_of_experience"])
        self.assertTrue(user.check_password(data["password1"]))

    def test_update_redactor(self) -> None:
        data = {
            "username": "testuser1",
            "first_name": "test first name",
            "last_name": "test last name",
            "email": "test@mail.com",
            "years_of_experience": 10,
        }
        self.client.post(
            path=reverse("editor:redactor-update", kwargs={"pk": 1}),
            data=data
        )
        user = Redactor.objects.get(pk=1)
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.years_of_experience, data["years_of_experience"])

    def test_delete_redactor(self) -> None:
        self.client.post(reverse("editor:redactor-delete", kwargs={"pk": 1}))
        self.assertEqual(Redactor.objects.count(), 0)
