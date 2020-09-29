from django.urls import path
from .views import ClientActivationDeactivationList, ClientStatusUpdate

urlpatterns = [
    path('activation-deactivation', ClientActivationDeactivationList.as_view(), name='activation/deactivation_list'),
    path('<int:pk>/activation', ClientStatusUpdate.as_view(), name='client_activation'),
    path('<int:pk>/deactivation', ClientStatusUpdate.as_view(), name='client_deactivation'),
]
