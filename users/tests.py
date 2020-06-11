from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class RegistrationTestCase1(APITestCase):
    url = reverse('register')

    def test_all_fields(self):
        data = {
            'email': 'marie@email.com', 'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '123qwer',
            'password': 'i-keep-jumping', "username": "marie"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'email': 'marie@email.com', 'first_name': 'Marie', 'last_name': 'Snyder',
                                         'passport_number': '123qwer', 'username': 'marie'})


    def test_missing_email_field(self):
        data = {
            'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '123qwer',
            'password': 'i-keep-jumping', 'username': 'marie'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["This field is required."]})


class RegistrationTestCase2(APITestCase):
    url = reverse('register')

    def setUp(self):
        User.objects.create_user(email='marie@email.com', first_name='Marie', last_name='Snyder',
                                 passport_number='123qwer', password='i-keep-jumping', username="marie")

    def test_email_already_exists(self):
        data = {
            'email': 'marie@email.com', 'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '1234qwer',
            'password': 'i-keep-jumping', "username": "anna"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["user with this email address already exists."]})

    def test_passport_number_already_exists(self):
        data = {
            'email': 'anna@email.com', 'first_name': 'Anna', 'last_name': 'Reed', 'passport_number': '123qwer',
            'password': 'i-keep-running', "username": "anna"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"passport_number": ["user with this passport number already exists."]})

    def test_email_and_passport_number_already_exist(self):
        data = {
            'email': 'marie@email.com', 'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '123qwer',
            'password': 'i-keep-jumping', "username": "anna"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["user with this email address already exists."],
                                         "passport_number": ["user with this passport number already exists."]})
