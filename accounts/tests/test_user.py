from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from accounts.models import User


class AnimalTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # this mimics a signup process with information collected
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="john@email.com"
            )
        self.user_2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="jane@email.com"
            )

    def test_user_signup(self):

        response = self.client.post(reverse('users-signup'))
        self.assertEqual(response.status_code, 400)

        signup_data = {
            "first_name": "Janet",
            "last_name": "Doe",
            "email": "janet@email.com"
        }

        response = self.client.post(reverse('users-signup'), data=signup_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_if_signup_info_exists(self):
        self.assertEqual(self.user_2.first_name, "Jane")
