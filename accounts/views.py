from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from .models import User


class RegistrationAPIView(CreateAPIView):
    """User's endpoint for registration"""

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer






