from django.urls import path
from .views import (ClientActivationAPIView, ClientDeactivationAPIView,
                    RegistrationAPIView, LoginAPIView, LogoutAPIView, ClientBalanceAPIView)


urlpatterns = [
    path('activation/', ClientActivationAPIView.as_view(), name='active'),
    path('deactivation/', ClientDeactivationAPIView.as_view(), name='not active'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='log in'),
    path('logout/<int:pk>/', LogoutAPIView.as_view(), name='log out'),
    path('balance/<int:pk>/', ClientBalanceAPIView.as_view(), name='balance'),
]