from django.test import TestCase

from editor.forms import (
    TopicForm,
    TopicSearchForm,
    RedactorCreationForm
)
from editor.models import Newspaper


class FormsTests(TestCase):

    def test_topic_form_with_name_newspapers_is_valid(self) -> None:
        form_data = {
            "name": "Test topic",
            "newspapers": (
                Newspaper.objects.create(
                    title="Test title",
                    content="Test content"
                ),
                Newspaper.objects.create(
                    title="Test title 2",
                    content="Test content 2"
                )
            )
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
            "newspapers": (
                Newspaper.objects.create(
                    title="Test title",
                    content="Test content",
                ),
            )
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
