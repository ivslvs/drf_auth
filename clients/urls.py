from django.urls import path
from .views import ClientBalanceAPIView, ClientUnregisterAPIView

urlpatterns = [
    path('balance/<int:pk>/', ClientBalanceAPIView.as_view(), name='balance'),
    path('deletion/<int:pk>/', ClientUnregisterAPIView.as_view(), name='deletion'),

]
