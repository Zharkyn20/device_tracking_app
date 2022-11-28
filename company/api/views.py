import jwt
import json
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from company.models import CustomUser
from config.settings import SECRET_KEY
from company.api.serializers import (
    CompanyRegistrationSerializer,
    CustomUserLoginSerializer)


class CompanyRegistrationView(generics.CreateAPIView):
    """
    Company registration endpoint
    """
    serializer_class = CompanyRegistrationSerializer

    @swagger_auto_schema(tags=['Company'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomUserLoginView(generics.CreateAPIView):
    serializer_class = CustomUserLoginSerializer

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status="400")

        email = request.data['email']
        password = request.data['password']
        user = get_object_or_404(CustomUser, email=email)
        if not user.check_password(password):
            return Response({'Error': "Invalid username/password"}, status="400")

        if not user:
            return Response(
                json.dumps({'Error': "Invalid credentials"}),
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

        payload = {
            'id': user.id,
            'email': user.email,
        }
        jwt_token = {'token': jwt.encode(payload, SECRET_KEY)}

        return Response(
            json.dumps(jwt_token),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )
