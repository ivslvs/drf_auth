from .serializers import ActivationDeactivationSerializer, UserStatusUpdateSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser
from accounts.models import User


class ClientActivationList(ListAPIView):
    """Manager's endpoint to see the clients list for activation"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(status='RA', is_active=False)
    serializer_class = ActivationDeactivationSerializer


class ClientDeactivationList(ListAPIView):
    """Manager's endpoint to see all deactivated clients"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(status='RD', is_active=True)
    serializer_class = ActivationDeactivationSerializer


class ClientStatusUpdate(UpdateAPIView):
    """Manager's endpoint for client deactivation"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserStatusUpdateSerializer
