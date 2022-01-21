from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User


class AnimalTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # this mimics a signup process with information collected
        self.user = User.objects.create(first_name="John", last_name="Doe")
        self.user_2 = User.objects.create(first_name="Jane", last_name="Doe")

    def test_user_signup(self):
        self.assertEqual(self.user.first_name, "John")

    def test_if_signup_info_exists(self):
        self.assertEqual(self.user_2.first_name, "Jane")
