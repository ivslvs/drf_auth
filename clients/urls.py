from django.urls import path
from .views import ClientBalanceAPIView, ClientDeletionAPIView

urlpatterns = [
    path('balance/<int:pk>/', ClientBalanceAPIView.as_view(), name='balance'),
    path('deletion/<int:pk>/', ClientDeletionAPIView.as_view(), name='deletion'),

]
