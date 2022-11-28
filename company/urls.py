from django.urls import path

from company.api.views import (
    CompanyRegistrationView,
    CustomUserLoginView
)


urlpatterns = [
    path("registration/", CompanyRegistrationView.as_view(), name='company'),
    path("login/", CustomUserLoginView.as_view(), name='login'),
]