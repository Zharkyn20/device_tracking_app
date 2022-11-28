from rest_framework import serializers

from company.models import Company
from device.models import (
    Device,
    DeviceDelegation,
)


class DeviceCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        write_only=True,
        required=True,
    )

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if user.is_company:
            name_values = Device.objects.filter(company__company_user=user).values_list('name', flat=True)
            company = Company.objects.get(company_user=user)
        else:
            company = user.company
            name_values = Device.objects.filter(company=company).values_list('name', flat=True)

        if validated_data['name'] in name_values:
            raise serializers.ValidationError(
                {"name": "This device already exists."}
            )

        device = Device.objects.create(
            company=company,
            name=validated_data['name']
        )
        device.save()

        return device

    class Meta:
        model = Device
        fields = ("name",)


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = '__all__'


class DeviceDelegationCreateSerializer(serializers.ModelSerializer):
    check_out_date = serializers.DateField()
    return_date = serializers.DateField()
    condition_before = serializers.CharField()

    def create(self, validated_data):
        delta = validated_data['return_date'] - validated_data['check_out_date']
        if delta.days < 0:
            raise serializers.ValidationError(
                {'return_date': 'Invalid return date'}
            )

        validated_data['duration_days'] = delta.days

        device_delegation = DeviceDelegation.objects.create(
            **validated_data
        )
        device_delegation.save()

        return device_delegation

    class Meta:
        model = DeviceDelegation
        fields = (
            'device',
            'check_out_date',
            'return_date',
            'condition_before',
        )


class DeviceDelegationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceDelegation
        fields = '__all__'
