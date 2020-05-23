from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import BalanceSerializers, ClientDeletionSerializer
from accounts.models import Balance, User


class ClientBalanceAPIView(RetrieveAPIView):
    """Client's endpoint to see Balance"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Balance.objects.all()  # Balance.objects.get(email=pk).balance
    serializer_class = BalanceSerializers


class ClientDeletionAPIView(UpdateAPIView):
    """Client's endpoint to leave the system"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ClientDeletionSerializer
