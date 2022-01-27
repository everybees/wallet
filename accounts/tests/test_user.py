from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from accounts.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # this mimics a signup process with information collected
        self.user = User.objects.create(
            first_name="John", last_name="Doe", email="john@email.com", username="john", password="my_password"
        )

        self.elite_user_data = {
            "first_name": "Janet",
            "last_name": "Doe",
            "email": "janet@email.com",
            "username": "janet",
            "password": "my_password",
            "user_type": "elite"
        }

        self.user_2 = User.objects.create(
            first_name="Jane", last_name="Doe", email="jane@email.com", username="jane", password="my_password"
        )

    def test_user_signup(self):
        response = self.client.post(reverse('users-signup'))
        self.assertEqual(response.status_code, 400)

        signup_data = {
            "first_name": "Janet",
            "last_name": "Doe",
            "email": "janet@email.com",
            "username": "janet",
            "password": "my_password"
        }

        response = self.client.post(reverse('users-signup'), data=signup_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_if_signup_info_exists(self):
        self.assertEqual(self.user_2.first_name, "Jane")

    def test_can_demote_user(self):
        response = self.client.post(reverse('users-signup'), data=self.elite_user_data, format='json')
        self.assertEqual(response.status_code, 201)
        demoted_user = self.client.put(reverse('users-demote-user'), data=response.data)

        self.assertEqual(demoted_user.data['user_type'], "noob")
