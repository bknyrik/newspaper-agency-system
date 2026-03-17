from django.test import TestCase
from django.contrib.auth import get_user_model

from editor.forms import (
    TopicForm,
    TopicSearchForm,
    NewspaperSearchForm,
    RedactorCreationForm,
    RedactorUpdateForm,
    RedactorSearchForm,
)
from editor.models import Newspaper, Topic


class FormsTests(TestCase):

    def setUp(self) -> None:
        self.newspapers = (
            Newspaper.objects.create(
                title="Test title",
                content="Test content"
            ),
            Newspaper.objects.create(
                title="Test title 2",
                content="Test content 2"
            )
        )

    def test_topic_form_with_name_newspapers_is_valid(self) -> None:
        form_data = {
            "name": "Test topic",
            "newspapers": self.newspapers
        }
        topic_form = TopicForm(data=form_data)
        self.assertTrue(topic_form.is_valid())
        self.assertEqual(topic_form.cleaned_data["name"], form_data["name"])
        self.assertEqual(
            tuple(topic_form.cleaned_data["newspapers"]),
            form_data["newspapers"]
        )

    def test_topic_search_form_with_name_is_valid(self) -> None:
        form_data = {"name": "test"}
        topic_search_form = TopicSearchForm(data=form_data)
        self.assertTrue(topic_search_form.is_valid())
        self.assertEqual(topic_search_form.cleaned_data, form_data)

    def test_redactor_creation_form_with_years_of_experience_newspapers_is_valid(
        self
    ) -> None:
        form_data = {
            "username": "testuser",
            "password1": "testpass12345",
            "password2": "testpass12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "email": "test@mail.com",
            "years_of_experience": 10,
            "newspapers": self.newspapers
        }
        rc_form = RedactorCreationForm(data=form_data)
        self.assertTrue(rc_form.is_valid())
        self.assertEqual(
            rc_form.cleaned_data["years_of_experience"],
            form_data["years_of_experience"]
        )
        self.assertTrue(
            tuple(rc_form.cleaned_data["newspapers"]),
            form_data["newspapers"]
        )

    def test_redactor_form_with_years_of_experience_newspapers_is_valid(
        self
    ) -> None:
        redactor = get_user_model().objects.create_user(
            username="testuser",
            password="testpass12345"
        )
        form_data = {
            "username": "testuser",
            "first_name": "Test first",
            "last_name": "Test last",
            "email": "test@mail.com",
            "years_of_experience": 10,
            "newspapers": self.newspapers
        }
        redactor_form = RedactorUpdateForm(data=form_data, instance=redactor)
        self.assertTrue(redactor_form.is_valid())
        self.assertEqual(
            redactor_form.cleaned_data["years_of_experience"],
            form_data["years_of_experience"]
        )
        self.assertEqual(
            tuple(redactor_form.cleaned_data["newspapers"]),
            form_data["newspapers"]
        )

    def test_redactor_search_form_is_valid(self) -> None:
        form_data = {
            "username": "testuser",
            "years_of_experience": 5
        }
        rs_form = RedactorSearchForm(data=form_data)
        self.assertTrue(rs_form.is_valid())
        self.assertEqual(rs_form.cleaned_data, form_data)


    def test_newspaper_search_form_is_valid(self) -> None:
        form_data = {
            "title": "Test",
            "topics": (
                Topic.objects.create(name="Test topic"),
            )
        }
        ns_form = NewspaperSearchForm(data=form_data)
        self.assertTrue(ns_form.is_valid())
        self.assertEqual(ns_form.cleaned_data["title"], form_data["title"])
        self.assertEqual(
            tuple(ns_form.cleaned_data["topics"]),
            form_data["topics"]
        )
