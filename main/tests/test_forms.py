from django.test import TestCase
from django.urls import reverse

from main.forms import CreateLocationForm
from users.models import User


class TestForms(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@mail.com", password="testpassword"
        )
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("main:favorites"))

    def test_favorites_form(self):
        form = self.response.context["form"]
        self.assertTrue(isinstance(form, CreateLocationForm))
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_favorites_form_validation_empty(self):
        form = CreateLocationForm(data={"name": ""})
        self.assertFalse(form.is_valid())    

