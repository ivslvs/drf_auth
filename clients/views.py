from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import BalanceSerializers, ClientUnregisterSerializer
from users.models import Balance, User


class ClientBalanceAPIView(RetrieveAPIView):
    """Client's endpoint to see Balance"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializers

    def get_queryset(self):
        return self.queryset.filter(client=self.request.user)


class ClientUnregisterAPIView(UpdateAPIView):
    """Client's endpoint to leave the system"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ClientUnregisterSerializer

