from django.urls import path
from .views import ClientActivationDeactivationList, ClientUnregisterUpdate


urlpatterns = [
    path('activation_deactivation/', ClientActivationDeactivationList.as_view(), name='activation/deactivation_list'),
    path('activation/<int:pk>/', ClientUnregisterUpdate.as_view(), name='client_activation'),
    path('deactivation/<int:pk>/', ClientUnregisterUpdate.as_view(), name='client_deactivation'),
]