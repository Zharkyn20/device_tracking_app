from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from company.api.serializers import CompanyRegistrationSerializer


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