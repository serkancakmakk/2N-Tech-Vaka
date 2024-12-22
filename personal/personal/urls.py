from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API dökümantasyonu için schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Çalışan Yönetimi API",
        default_version='v1',
        description="Çalışanların izin durumlarını ve mesai saatlerini takip etmek için kullanılan API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@yourcompany.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('personal_track.urls')),  # Uygulamanızın URL'leri burada
    # Swagger UI için URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
