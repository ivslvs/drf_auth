from .serializers import ActivationDeactivationSerializer, ClientStatusSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser
from users.models import User


class ClientActivationDeactivationList(ListAPIView):
    """Manager's endpoint to see the clients list for activation
    and list for deactivation"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = ActivationDeactivationSerializer
    filter_fields = ['status']


class ClientUnregisterUpdate(UpdateAPIView):
    """Manager's endpoint for client deactivation"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = ClientStatusSerializer
