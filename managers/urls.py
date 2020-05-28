from django.urls import path
from .views import ClientActivationList, ClientDeactivationList, ClientStatusUpdate


urlpatterns = [
    path('activation/', ClientActivationList.as_view(), name='activation_list'),
    path('activation/<int:pk>/', ClientStatusUpdate.as_view(), name='client_activation'),
    path('deactivation/', ClientDeactivationList.as_view(), name='deactivation_list'),
    path('deactivation/<int:pk>/', ClientStatusUpdate.as_view(), name='client_deactivation'),
]