from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class LoginTestCase(APITestCase):

    def setUp(self):
        User.objects.create_user(email='anna@email.com', first_name='Anna', last_name='Reed',
                                 passport_number='678qwert', password='i-keep-running', username="anna")
        User.objects.filter(id=1).update(is_active=True)

    def test_all_fields(self):
        response = self.client.login(username='anna', password='i-keep-running')
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
        # TypeError: Field 'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x7f76c85ea470>.

        User.objects.create_user(username='marie', email='marie@email.com', first_name='Marie', last_name='Snyder',
                                 passport_number='123qwer', password='i-keep-jumping')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"client": 1, "balance": "0.0000000000"})
