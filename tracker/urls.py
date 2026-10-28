"""URL routing for tracker API with DRF DefaultRouter."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"departments", views.DepartmentViewSet, basename="department")
router.register(r"employees", views.EmployeeViewSet, basename="employee")
router.register(r"assignments", views.AssignmentViewSet, basename="assignment")

urlpatterns = [
    path("health/", views.health_check, name="health-check"),
    path("", include(router.urls)),
]
