from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from main.models import Location
from users.models import User


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@mail.com", password="testpassword"
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_post_request_with_correct_data(self):
        response = self.client.post(reverse("main:index"), {"city": "Moscow"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("weather_data", response.context)

    def test_post_request_with_invalid_city(self):
        response = self.client.post(reverse("main:index"), {"city": "InvalidCity"})
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(
            "Ошибка. Введите корректное название города и попробуйте позже!",
            messages[0],
        )

    def test_post_request_without_city(self):
        response = self.client.post(reverse("main:index"), {})
        self.assertEqual(response.status_code, 200)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Ошибка. Введите корректное название города.", messages)


class FavoritesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@mail.com", password="testpassword"
        )
        self.client = Client()
        self.location = Location.objects.create(
            name="Moscow", latitude=55.7504, longitude=37.6175, user=self.user
        )

    def test_get_request_unauthorized(self):
        response = self.client.get(reverse("main:favorites"))
        self.assertEqual(response.status_code, 302)

    def test_get_request_authorized(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("main:favorites"))
        self.assertEqual(response.status_code, 200)

    def test_favorite_locations(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("main:favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("weather_data_list", response.context)
        self.assertIn("Moscow", response.content.decode())
        self.assertNotIn("London", response.content.decode())
