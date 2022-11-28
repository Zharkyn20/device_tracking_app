from django.urls import path, include
from rest_framework.routers import DefaultRouter

from device.api.views import (
    DeviceViewSet,
    DeviceDelegationViewSet
)

router = DefaultRouter()

router.register("device", DeviceViewSet, basename="device")
router.register('device_delegation', DeviceDelegationViewSet, basename='device_dlegation')


urlpatterns = [
    path("", include(router.urls)),
]