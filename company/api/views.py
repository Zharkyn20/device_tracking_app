import jwt
import json
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from utils import permissions
from company.models import (
    Company,
    CustomUser,
    Staff,
    Employee,
)
from config.settings import SECRET_KEY
from company.api.serializers import (
    CompanyRegistrationSerializer,
    CustomUserLoginSerializer,
    StaffRegistrationSerializer,
    StaffSerializer,
    EmployeeSerializer,
    EmployeeRegistrationSerializer,
)


class CompanyRegistrationView(generics.CreateAPIView):
    """
    Company registration endpoint
    """

    serializer_class = CompanyRegistrationSerializer

    @swagger_auto_schema(tags=["Company"])
    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        company = Company.objects.create(
            company_user=user, company_name=request.data["company_name"]
        )
        company.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomUserLoginView(generics.CreateAPIView):
    serializer_class = CustomUserLoginSerializer

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({"Error": "Please provide username/password"}, status="400")

        email = request.data["email"]
        password = request.data["password"]
        user = get_object_or_404(CustomUser, email=email)
        if not user.check_password(password):
            return Response({"Error": "Invalid username/password"}, status="400")

        if not user:
            return Response(
                json.dumps({"Error": "Invalid credentials"}),
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )

        payload = {
            "id": user.id,
            "email": user.email,
        }
        jwt_token = {"token": jwt.encode(payload, SECRET_KEY)}

        return Response(
            json.dumps(jwt_token),
            status=status.HTTP_200_OK,
            content_type="application/json",
        )


class StaffViewSet(ModelViewSet):
    serializer_class = StaffRegistrationSerializer
    permission_classes = [IsAuthenticated, permissions.IsCompany]

    def create(self, request, *args, **kwargs):
        user = request.user

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = serializer.save()

        staff = Staff.objects.create(
            user=staff, company=Company.objects.get(company_user=user)
        )
        staff.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return StaffSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Staff.objects.filter(company__company_user=self.request.user)


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return EmployeeSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Employee.objects.filter(company__company_user=self.request.user)
