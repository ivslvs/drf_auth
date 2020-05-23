from django.contrib import admin
from django.urls import path, include
from accounts.views import RegistrationAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    #rest-auth
    path('rest-auth/', include('rest_auth.urls')),

    #custom register
    path('register/', RegistrationAPIView.as_view(), name='register'),

    #jwt
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('api/v1/clients/', include('clients.urls')),
    path('api/v1/managers/', include('managers.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # djoser
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]
