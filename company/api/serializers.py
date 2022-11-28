from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from company.models import Company, CustomUser


class CompanyRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all(), message="This email already used")
        ],
    )
    username = serializers.CharField(
        write_only=True,
        required=True,
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_verification = serializers.CharField(write_only=True, required=True)
    company_name = serializers.CharField(
        write_only=True,
        required=True,
        validators=
        [UniqueValidator(queryset=Company.objects.all(), message="Company with this name already exists")]
    )

    class Meta:
        model = Company
        fields = (
            "id",
            "username",
            "email",
            "password",
            "password_verification",
            "company_name"
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_verification"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            is_company=True
        )

        user.set_password(validated_data["password"])
        user.save()

        company = Company.objects.create(
            company_user=user,
            company_name=validated_data["company_name"]
        )

        return user


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(validators=[validate_password, ])
