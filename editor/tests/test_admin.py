from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
        )
        self.client.force_login(user=self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="testuser",
            password="test12345",
            years_of_experience=14
        )

    def test_redactor_years_of_experience_listed(self) -> None:
        url = reverse("admin:editor_redactor_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_years_of_experience_in_detail_page(self) -> None:
        url = reverse("admin:editor_redactor_change", args=[self.redactor.id])
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_years_of_experience_in_add_page(self) -> None:
        url = reverse("admin:editor_redactor_add")
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)
