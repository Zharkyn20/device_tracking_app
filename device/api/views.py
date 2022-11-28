from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from company.models import Company
from device.api.serializers import (
    DeviceCreateSerializer,
    DeviceSerializer,
    DeviceDelegationCreateSerializer,
    DeviceDelegationSerializer,
)
from device.models import DeviceDelegation, Device


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_company:
            company = Company.objects.get(staff__user=user)
            return Device.objects.filter(company=company)

        return Device.objects.filter(company__company_user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return DeviceSerializer
        return super().get_serializer_class()


class DeviceDelegationViewSet(ModelViewSet):
    serializer_class = DeviceDelegationCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if (
            self.action == "list"
            or self.action == "retrieve"
            or self.action == "partial_update"
        ):
            return DeviceDelegationSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if not user.is_company:
            company = Company.objects.get(staff__user=user)
            return DeviceDelegation.objects.filter(device__company=company)

        return DeviceDelegation.objects.filter(
            device__company__company_user=self.request.user
        )
