from django.contrib import admin

from company.models import Company, CustomUser, Staff, Employee
from device.models import Device


class StaffInline(admin.StackedInline):
    model = Staff


class EmployeeInline(admin.StackedInline):
    model = Employee


class DeviceInline(admin.StackedInline):
    model = Device


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        model = CustomUser


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [StaffInline, EmployeeInline, DeviceInline]

    class Meta:
        model = Company
