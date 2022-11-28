from django.db import models

from company.models import Company


class Device(models.Model):
    name = models.CharField(max_length=250)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='device_company'
    )

    def __str__(self):
        return self.name


class DeviceDelegation(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
    )
    duration_days = models.IntegerField(default=21)
    check_out_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    condition_before = models.TextField(default='test')
    condition_after = models.TextField(null=True, blank=True)

