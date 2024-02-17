from django.test import SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve

from main import views


class MainUrlsTests(SimpleTestCase):
    def test_index_url_resolves(self):
        response = self.client.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)

    def test_about_url_resolves(self):
        response = self.client.get(reverse("main:about"))
        self.assertEqual(response.status_code, 200)
    
    def test_favorites_url_resolves(self):
        response = self.client.get(reverse("main:favorites"))
        self.assertEqual(response.status_code, 302)
    
    def test_root_url_resolves(self):
        urls = [
            resolve('/'),
            resolve('/about/'),
            resolve('/favorites/'),
        ]
        for i, url in enumerate(urls, 1):
            if i == 1:
                self.assertEqual(url.func, views.index)
            elif i == 2:
                self.assertEqual(url.func, views.about)
            elif i == 3:
                self.assertEqual(url.func, views.favorites)
