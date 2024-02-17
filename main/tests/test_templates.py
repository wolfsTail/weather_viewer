from django.test import TestCase
from django.urls import reverse

from users.models import User


class TemplateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@mail.com", password="testpassword"
        )
        self.client.force_login(self.user)

    def test_index_template(self):
        response = self.client.get(reverse("main:index"))
        self.assertTemplateUsed(response, "main/index.html")
    
    def test_about_template(self):
        response = self.client.get(reverse("main:about"))
        self.assertTemplateUsed(response, "main/about.html")
    
    def test_favorites_template(self):
        response = self.client.get(reverse("main:favorites"))
        self.assertTemplateUsed(response, "main/favorites.html")
    
    def test_index_contains_correcet_html(self):
        response = self.client.get(reverse("main:index"))
        self.assertContains(response, "Weather viewer")
    
    def test_favorites_contains_correct_html(self):
        response = self.client.get(reverse("main:favorites"))
        self.assertContains(response, "Weather viewer")

    def test_about_not_contains_incorrect_html(self):
        response = self.client.get(reverse("main:about"))
        self.assertNotContains(response, "Weather Viewer LOL")
