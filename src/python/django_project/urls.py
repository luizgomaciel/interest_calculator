"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from src.python.django_project.initial_project_app.views import InitialProjectView

router = DefaultRouter()
router.register(r"api/projects", InitialProjectView, basename="project")

urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls

# path('projects/', InitialProjectListCreateView.as_view({'post': 'post'}), name='project-create'),
# path('projects/<int:project_id>/', InitialProjectListCreateView.as_view({'get': 'get'}), name='project-detail'),