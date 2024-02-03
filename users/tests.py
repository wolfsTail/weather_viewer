from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class RegistrationLoginLogoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.registration_url = reverse("users:registration")
        self.login_url = reverse("users:login")
        self.profile_url = reverse("users:profile")
        self.logout_url = reverse("users:logout")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Tester",
            "last_name": "User",
            "password": "testpassword123",
        }

    def test_registration(self):
        self.user_data.setdefault("confirm_password", "testpassword123")

        response = self.client.get(self.registration_url)
        self.assertEqual(
            response.status_code, 200
        )  # Проверяем доступность страницы регистрации

        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(
            response.status_code, 302
        )  # Проверяем редирект после успешной регистрации
        self.assertTrue(
            get_user_model().objects.filter(email=self.user_data["email"]).exists()
        )  # Проверяем, что пользователь был создан

    def test_login(self):
        get_user_model().objects.create_user(
            **self.user_data
        )  # Создаем пользователя для тестирования входа

        response = self.client.get(self.login_url)
        self.assertEqual(
            response.status_code, 200
        )  # Проверяем доступность страницы входа

        response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        self.assertEqual(
            response.status_code, 302
        )  # Проверяем редирект после успешного входа

    def test_profile(self):
        user = get_user_model().objects.create_user(
            **self.user_data
        )  # Создаем пользователя для тестирования профиля
        self.client.login(
            email=self.user_data["email"], password=self.user_data["password"]
        )  # Авторизуемся

        response = self.client.get(self.profile_url)
        self.assertEqual(
            response.status_code, 200
        )  # Проверяем доступность страницы профиля
        self.assertContains(
            response, self.user_data["email"]
        )  # Проверяем, что на странице есть email пользователя

    def test_logout(self):
        user = get_user_model().objects.create_user(
            **self.user_data
        )  # Создаем пользователя для тестирования выхода
        self.client.login(
            email=self.user_data["email"], password=self.user_data["password"]
        )  # Авторизуемся

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после выхода
        self.assertFalse(
            "_auth_user_id" in self.client.session
        )  # Проверяем, что пользователь вышел из системы
