
# from django.contrib import admin
# from django.urls import path
# from django.views.generic import RedirectView
# from rest_framework.routers import DefaultRouter
#
# from src.python.django_project.initial_project_app.views import InitialProjectView
#
# router = DefaultRouter()
# router.register(r"api/projects", InitialProjectView, basename="projects")
#
# urlpatterns = [
#     path('', RedirectView.as_view(url='api/projects', permanent=False), name='home'),
#     path('admin/', admin.site.urls),
# ] + router.urls

# python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from src.python.django_project.initial_project_app.views import InitialProjectView

router = DefaultRouter()
router.register(r'projects', InitialProjectView, basename='projects')

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="Descrição da API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', RedirectView.as_view(url='api/projects', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger(<format>\\.json|\\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
