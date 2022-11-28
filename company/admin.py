from django.contrib import admin

from company.models import Company, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    class Meta:
        model = CustomUser


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    class Meta:
        model = Company
