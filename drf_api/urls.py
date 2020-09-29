from django.contrib import admin
from django.urls import path, include
from users.views import RegistrationAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('register/', RegistrationAPIView.as_view(), name='register'),

    path('api/v1/clients/', include('clients.urls')),
    path('api/v1/managers/clients/', include('managers.urls')),


]
