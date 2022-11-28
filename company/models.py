from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_company = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Company(models.Model):
    company_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=250)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "Companies"


class Staff(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="company_user"
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = "Staff"


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
