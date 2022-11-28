from django.db import models

from company.models import Company, Employee


class Device(models.Model):
    name = models.CharField(max_length=250)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="device_company"
    )

    def __str__(self):
        return self.name


class DeviceDelegation(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
    )
    duration_days = models.IntegerField()
    check_out_date = models.DateField()
    return_date = models.DateField()
    condition_before = models.TextField()
    condition_after = models.TextField(null=True, blank=True)
