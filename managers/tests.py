from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class ActivationDeactivationTestCase(APITestCase):
    activation_deactivation_list = reverse('activation/deactivation_list')
    deletion = reverse('deletion', kwargs={"pk": 15})
    client_activation = reverse('client_activation', kwargs={"pk": 9})
    client_deactivation = reverse('client_deactivation', kwargs={"pk": 13})

    url = 'http://testserver'

    url_token = 'http://127.0.0.1:8000/rest-auth/login/'

    def setUp(self):
        User.objects.create_user(email='anna@email.com', first_name='Anna', last_name='Reed',
                                 passport_number='678qwert', password='i-keep-running', username="anna")
        User.objects.create_user(email='peter@email.com', first_name='Peter', last_name='Snow',
                                 passport_number='987qwert', password='i-keep-swimming', username="peter")
        User.objects.create_user(email='dan@email.com', first_name='Dan', last_name='Snow',
                                 passport_number='62772qwert', password='i-keep-jumping', username="dan")
        User.objects.filter(username='anna').update(is_superuser=True, is_staff=True)
        User.objects.filter(last_name='Snow').update(is_active=False, status='RA')
        self.superuser_token = self.client.post(self.url_token, data={'username': 'anna', 'password': "i-keep-running"},
                                                format='json')
        self.token_key = self.superuser_token.data['key']

    def test_activation(self):
        response = self.client.get(self.activation_deactivation_list + '?status=RA',
                                   HTTP_AUTHORIZATION='Token ' + self.token_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": 7, "email": "peter@email.com"},
                                         {"id": 8, "email": "dan@email.com"}])

    def test_client_activation(self):
        response = self.client.put(self.client_activation, {"email": "anna@email.com"},
                                   HTTP_AUTHORIZATION='Token ' + self.token_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 9, "status": "A", "is_active": True})

    def test_deactivation(self):
        User.objects.filter(last_name='Snow').update(status='RD', is_active=True)
        response = self.client.get(self.activation_deactivation_list + '?status=RD',
                                   HTTP_AUTHORIZATION='Token ' + self.token_key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": 19, "email": "peter@email.com"},
                                         {"id": 20, "email": "dan@email.com"}])

    def test_client_deactivation(self):
        User.objects.filter(id=13).update(status='RD')
        response = self.client.put(self.client_deactivation, {"email": "peter@email.com"},
                                   HTTP_AUTHORIZATION='Token ' + self.token_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_deletion(self):
        data = {
            "username": "anna",
            "email": "anna@email.com",
            "password": "i-keep-running",
            "passport_number": "678qwert"
        }
        response = self.client.put(self.deletion, data, HTTP_AUTHORIZATION='Token ' + self.token_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 15, "email": "anna@email.com"})


