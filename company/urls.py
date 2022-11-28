from django.urls import path

from company.api.views import CompanyRegistrationView


urlpatterns = [
    path("registration/", CompanyRegistrationView.as_view(), name='company'),
]