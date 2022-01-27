from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from accounts.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # this mimics a signup process with information collected
        self.user_data = {
            'first_name': "John",
            'last_name': "Doe",
            'email': "john@email.com",
            'username': "john",
            'password': "my_password"
        }

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

    def test_can_demote_elite_user(self):
        response = self.client.post(reverse('users-signup'), data=self.elite_user_data, format='json')
        self.assertEqual(response.status_code, 201)
        demoted_user = self.client.put(reverse('users-demote-user'), data=response.data)

        self.assertEqual(demoted_user.data['user_type'], "noob")

    def test_cannot_demote_noob_user(self):
        # given
        response = self.client.post(reverse("users-signup"), data=self.user_data, format='json')
        # when
        noob_user_response = self.client.put(reverse("users-demote-user"), response.data, format="json")
        # assert
        self.assertEqual(noob_user_response.status_code, 400)

        pass

    def test_can_promote_noob_user(self):
        response = self.client.post(reverse("users-signup"), data=self.user_data, format='json')
        self.assertEqual(response.data['id'], 4)
        promoted_user_response = self.client.put(reverse("users-promote-user"), data=response.data, format="json")
        self.assertEqual(promoted_user_response.data['user_type'], 'elite')

    def test_cannot_promote_elite_user(self):
        # given
        response = self.client.post(reverse('users-signup'), data=self.elite_user_data, format='json')
        # when
        elite_user_response = self.client.put(reverse('users-promote-user'), data=response.data, format='json')
        # assert
        self.assertEqual(elite_user_response.status_code, 400)
