from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegistrationSerializer, LoginSerializer
from .models import Balance, Client
from rest_framework.authtoken.models import Token


class ClientActivationAPIView(GenericAPIView):
    """Manager's endpoint to see the list of pending
    requests for approval"""

    authentication_classes = [TokenAuthentication]
    permission_classes = []  # тут должен быть установлен пермишенс для манагеров

    def get(self, request):
        activation_pk = [i.pk for i in Client.objects.filter(status='requires activation', is_active=False)]
        if activation_pk:
            # 1) смущает жосткая ссылка, норм\не норм такое писать?
            urls = ['http://127.0.0.1:8000/admin/accounts/client/' + str(pk) + '/change/' for pk in activation_pk]
            return Response({'Clients requiring activation': urls})
        return Response({'No clients for activation.'})


class ClientDeactivationAPIView(GenericAPIView):
    """Manager's endpoint to see all closed accounts in order to
    confirm the deletion"""
    authentication_classes = [TokenAuthentication]
    permission_classes = []  # тут должен быть установлен пермишенс для манагеров

    def get(self, request):
        deactivation_pk = [i.pk for i in Client.objects.filter(status='requires deactivation', is_active=True)]
        if deactivation_pk:
            urls = ['http://127.0.0.1:8000/admin/accounts/client/' + str(pk) + '/change/' for pk in deactivation_pk]
            return Response({'Clients requiring deactivation': urls})
        return Response({'No clients for deactivation.'})


class RegistrationAPIView(APIView):
    """User's registration"""

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()

        token = Token.objects.get(user=account).key

        # 2) уместно нижние две строчки писать во втюхе? или лучше писать в сериалайзере\моделе?
        user = Client.objects.get(email=request.data['email'])
        Balance.objects.create(email=user, balance=0)  # во время регистрации у юзера создается поле с балансом

        return Response({'response': 'Successfully registered new user.', 'pk': account.pk, 'status': account.status,
                         'email': account.email, 'first_name': account.first_name, 'last_name': account.last_name,
                         'passport_number': account.passport_number, 'token': token},
                        status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """Log in"""

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'response': 'Successfully logged in.'})


class LogoutAPIView(APIView):
    """Log out"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        Client.objects.filter(pk=pk).update(status='requires deactivation')  # меняется status по которому манагеры деактивируют пользователя
        return Response({'response': 'Successfully logged out.'})


class ClientBalanceAPIView(APIView):
    """Balance"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        balance = Balance.objects.get(email=pk).balance
        return Response({'balance': balance})

