from django.contrib import admin

from device.models import DeviceDelegation, Device


class DeviceDelegationInline(admin.StackedInline):
    model = DeviceDelegation


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    inlines = [
        DeviceDelegationInline
    ]

    class Meta:
        model = Device
