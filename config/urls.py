"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import include, path


def api_logout(request):
    """Logs out and redirects directly to the login page to enter new credentials."""
    logout(request)
    return redirect("/api-auth/login/?next=/api/assignments/")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tracker.urls")),
    path("api-auth/logout/", api_logout, name="logout"),
    path("api-auth/", include("rest_framework.urls")),
]
