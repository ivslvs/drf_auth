from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Client


# 1) регистрацию тестирую аж 2 класса
# в одном классе нет setUP, во втором есть, поэтому я разделила тесты
# меня смущает избыточность. 1 апи - 1 класс тестов, так правильнее?
# совмещала и оно не працювало

class RegistrationTestCase1(APITestCase):
    url = reverse('register')

    def test_all_fields(self):
        data = {
            'email': 'marie@email.com', 'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '123qwer',
            'password': 'i-keep-jumping', 'password2': 'i-keep-jumping'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"response": "Successfully registered new user.",
                                         "pk": response.data['pk'], "status": "requires activation",
                                         "email": "marie@email.com",
                                         "first_name": "Marie", "last_name": "Snyder", "passport_number": "123qwer",
                                         "token": response.data['token']})

    def test_missing_email_field(self):
        data = {
            'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '123qwer',
            'password': 'i-keep-jumping', 'password2': 'i-keep-jumping'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["This field is required."]})

    def test_password_does_not_match(self):
        data = {
            'email': 'marie@email.com', 'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '123qwer',
            'password': 'i-keep-jumping', 'password2': '-keep-jumping'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"password": "Passwords must match."})


class RegistrationTestCase2(APITestCase):
    url = reverse('register')

    def setUp(self):
        Client.objects.create_user(email='marie@email.com', first_name='Marie', last_name='Snyder',
                                   passport_number='123qwer', password='i-keep-jumping')

    def test_email_already_exists(self):
        data = {
            'email': 'marie@email.com', 'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '1234qwer',
            'password': 'i-keep-jumping', 'password2': 'i-keep-jumping'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["client with this email address (case-sensitive) already exists."]})

    def test_passport_number_already_exists(self):
        data = {
            'email': 'anna@email.com', 'first_name': 'Anna', 'last_name': 'Reed', 'passport_number': '123qwer',
            'password': 'i-keep-running', 'password2': 'i-keep-running'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"passport_number": ["client with this passport number already exists."]})

    def test_email_and_passport_number_already_exist(self):
        data = {
            'email': 'marie@email.com', 'first_name': 'Marie', 'last_name': 'Snyder', 'passport_number': '123qwer',
            'password': 'i-keep-jumping', 'password2': 'i-keep-jumping'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["client with this email address (case-sensitive) already exists."],
                                         "passport_number": ["client with this passport number already exists."]})


class LoginTestCase(APITestCase):
    url = reverse('log in')

    def setUp(self):
        Client.objects.create_user(email='anna@email.com', first_name='Anna', last_name='Reed',
                                   passport_number='678qwert', password='i-keep-running')
        Client.objects.filter(pk=1).update(is_active=True)

    def test_all_fields(self):
        response = self.client.login(email='anna@email.com', password='i-keep-running')
        self.assertTrue(response, True)
        # self.assertEqual(response.data, {"response":"Successfully logged in."})

    def test_wrong_email(self):
        response = self.client.login(email='peter@email.com', password='i-keep-running')
        self.assertFalse(response, False)

    def test_wrong_password(self):
        response = self.client.login(email='anna@email.com', password='i-keep-swimming')
        self.assertFalse(response, False)

    def test_letter_case(self):
        response = self.client.login(email='ANNA@email.com', password='i-keep-running')
        self.assertFalse(response, False)



# 2) чтобы выполнить log out или просмотреть баланс, мне нужно отрпавить токен в запросе
# как это сделать в тестах - не разобралась

# class LogoutTestCase(APITestCase):
#     url = 'log out'
#
#     def setUp(self):
#         Client.objects.create_user(email='Peter@email.com', first_name='Peter', last_name='May',
#                                    passport_number='98765er', password='i-keep-lying')
#         Client.objects.filter(pk=1).update(is_active=True)
#
#         self.token = Token.objects.get(user_id=1).key
#         self.api_authentication()
#
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
#
#     def test_log_out(self):
#         response = self.client.get(self.url, kwargs={'pk': 1})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class ClientBalanceTestCase(APITestCase):
#     url = reverse('balance')
#
#     def test_client_balance(self):
#         Client.objects.create_user(email='marie@email.com', first_name='Marie', last_name='Snyder',
#                                    passport_number='123qwer', password='i-keep-jumping')
#         token = Token.objects.get(user_id=1)
#         response = self.client.get(self.url, kwargs={'pk': 1}, HTTP_AUTHORIZATION='Token ' + token.key)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivationDeactivationTestCase(APITestCase):
    act = reverse('active')
    deact = reverse('not active')

    def setUp(self):
        Client.objects.create_user(email='anna@email.com', first_name='Anna', last_name='Reed',
                                   passport_number='678qwert', password='i-keep-running')

    def test_activation(self):
        response = self.client.get(self.act)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deactivation(self):
        Client.objects.filter(pk=1).update(status='deactivation')
        response = self.client.get(self.deact)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
