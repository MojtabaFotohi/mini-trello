from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.i18n import i18n_patterns
from users.views import CustomTokenObtainPairView

#api docs
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Modern Trello API",
        default_version='v1',
        description="API documentation for Modern Trello project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', include('users.urls')),
    path('boards/', include('boards.urls')),
    path('lists/', include('lists.urls')),
    path('invitations/', include('invitations.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # Swagger UI
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns += i18n_patterns(
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    prefix_default_language=False,  
)







