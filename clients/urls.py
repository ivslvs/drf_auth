from django.urls import path
from .views import ClientBalanceAPIView, ClientUnregisterAPIView

urlpatterns = [
    path('<int:pk>/balance', ClientBalanceAPIView.as_view(), name='balance'),
    path('<int:pk>/deletion', ClientUnregisterAPIView.as_view(), name='deletion'),

]
