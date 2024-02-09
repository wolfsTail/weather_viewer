import unittest
from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse
from main.views import index

class IndexViewTests(TestCase):
    def test_index_view_with_valid_city(self):
        response = self.client.post('/', {'city': 'Moscow'})
        print(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertIn('weather_data', response.context)
        self.assertEqual(response.context['weather_data']['city'], 'Moscow')

    





