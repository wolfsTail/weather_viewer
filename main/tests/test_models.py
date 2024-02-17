from django.test import TestCase

from main.models import Location
from users.models import User


class LocationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.location = Location.objects.create(
            name="Test Location", latitude=1.0, longitude=1.0, user=self.user
        )

    def test_create_location(self):
        self.assertIsInstance(self.location, Location)

    def test_location_str(self):
        self.assertEqual(str(self.location), "Test Location: lat:1.0, lon:1.0")

    def test_save_and_retrieve_location(self):
        second_test_location = Location()
        second_test_location.name = "Second Test Location"
        second_test_location.latitude = 2.0
        second_test_location.longitude = 2.0
        second_test_location.user = self.user
        second_test_location.save()

        third_test_location = Location()
        third_test_location.name = "Third Test Location"
        third_test_location.latitude = 3.0
        third_test_location.longitude = 3.0
        third_test_location.user = self.user
        third_test_location.save()

        locations = Location.objects.all()
        self.assertEqual(locations.count(), 3)

        first = locations[0]
        second = locations[1]
        third = locations[2]

        self.assertEqual(first.name, "Test Location")
        self.assertEqual(first.latitude, 1.0)
        self.assertEqual(first.longitude, 1.0)
        self.assertEqual(second.name, "Second Test Location")
        self.assertEqual(third.longitude, 3.0)
