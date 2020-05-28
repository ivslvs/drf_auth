from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User


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
                                         'passport_number': '123qwer', })

    def test_missing_email_field(self):
        data = {
            'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '123qwer',
            'password': 'i-keep-jumping'
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
            'password': 'i-keep-jumping', "username": "marie"
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
            'password': 'i-keep-jumping', "username": "marie"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["user with this email address already exists."],
                                         "passport_number": ["user with this passport number already exists."]})


class LoginTestCase(APITestCase):

    def setUp(self):
        User.objects.create_user(email='anna@email.com', first_name='Anna', last_name='Reed',
                                 passport_number='678qwert', password='i-keep-running', username="anna")
        User.objects.filter(id=1).update(is_active=True)

    def test_all_fields(self):
        response = self.client.login(email='anna@email.com', password='i-keep-running')
        self.assertTrue(response, True)

    def test_wrong_email(self):
        response = self.client.login(email='peter@email.com', password='i-keep-running')
        self.assertFalse(response, False)

    def test_wrong_password(self):
        response = self.client.login(email='anna@email.com', password='i-keep-swimming')
        self.assertFalse(response, False)

    def test_letter_case(self):
        response = self.client.login(email='ANNA@email.com', password='i-keep-running')
        self.assertFalse(response, False)


class ClientBalanceTestCase(APITestCase):
    url = reverse('balance', kwargs={'pk': 1})

    def test_client_balance(self):
        User.objects.create_user(email='marie@email.com', first_name='Marie', last_name='Snyder',
                                 passport_number='123qwer', password='i-keep-jumping', username='marie')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"client": 1, "balance": "0.0000000000"})


class ActivationDeactivationTestCase(APITestCase):
    activation_list = reverse('activation_list')
    deactivation_list = reverse('deactivation_list')
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
        User.objects.filter(is_active=True).update(is_active=False)
        response = self.client.get(self.activation_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"client": self.url + reverse('client_activation', kwargs={'pk': 1})},
                                         {"client": self.url + reverse('client_activation', kwargs={'pk': 2})},
                                         {"client": self.url + reverse('client_activation', kwargs={'pk': 3})}])

    def test_client_activation(self):
        response = self.client.put(self.client_activation, {"email": "anna@email.com"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 1, "status": "RA", "is_active": True})

    def test_deactivation(self):
        User.objects.filter(status='RA').update(status='RD', is_active=True)
        response = self.client.get(self.deactivation_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"client": self.url + reverse('client_deactivation', kwargs={'pk': 1})},
                                         {"client": self.url + reverse('client_deactivation', kwargs={'pk': 2})},
                                         {"client": self.url + reverse('client_deactivation', kwargs={'pk': 3})}])

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
        self.assertEqual(response.data, {"pk": 1, "email": "anna@email.com"})
