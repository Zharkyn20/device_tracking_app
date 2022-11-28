from django.urls import path, include
from rest_framework.routers import DefaultRouter

from company.api.views import (
    CompanyRegistrationView,
    CustomUserLoginView,
    StaffViewSet,
    EmployeeViewSet,
)

router = DefaultRouter()

router.register("staff", StaffViewSet, basename="staff")
router.register("employee", EmployeeViewSet, basename="employee")


urlpatterns = [
    path("", include(router.urls)),
    path("company_registration/", CompanyRegistrationView.as_view(), name="company"),
    path("login/", CustomUserLoginView.as_view(), name="login"),
]
