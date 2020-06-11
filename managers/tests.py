from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class ActivationDeactivationTestCase(APITestCase):
    activation_deactivation_list = reverse('activation/deactivation_list')
    deletion = reverse('deletion', kwargs={"pk": 1})
    client_activation = reverse('client_activation', kwargs={"pk": 1})
    client_deactivation = reverse('client_deactivation', kwargs={"pk": 2})

    url = 'http://testserver'

    def setUp(self):
        User.objects.create_user(email='anna@email.com', first_name='Anna', last_name='Reed',
                                 passport_number='678qwert', password='i-keep-running', username="anna")
        User.objects.create_user(email='peter@email.com', first_name='Peter', last_name='Snow',
                                 passport_number='987qwert', password='i-keep-swimming', username="peter")
        User.objects.create_user(email='dan@email.com', first_name='Dan', last_name='Tomson',
                                 passport_number='62772qwert', password='i-keep-jumping', username="dan")

    def test_activation(self):
        User.objects.filter(is_active=True).update(is_active=False, status='RA')
        response = self.client.get(self.activation_deactivation_list + '?status=RA')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": 1, "email": "anna@email.com"},
                                         {"id": 2, "email": "peter@email.com"},
                                         {"id": 3, "email": "dan@email.com"}])

    def test_client_activation(self):
        response = self.client.put(self.client_activation, {"email": "anna@email.com"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 1, "status": "A", "is_active": True})

    def test_deactivation(self):
        User.objects.filter(status='A').update(status='RD', is_active=True)
        response = self.client.get(self.activation_deactivation_list + '?status=RD')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": 1, "email": "anna@email.com"},
                                         {"id": 2, "email": "peter@email.com"},
                                         {"id": 3, "email": "dan@email.com"}])

    def test_client_deactivation(self):
        User.objects.filter(id=2).update(status='RD')
        response = self.client.put(self.client_deactivation, {"email": "peter@email.com"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_deletion(self):
        data = {
            "username": "anna",
            "email": "anna@email.com",
            "password": "i-keep-running",
            "passport_number": "678qwert"
        }
        response = self.client.put(self.deletion, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 1, "email": "anna@email.com"})
