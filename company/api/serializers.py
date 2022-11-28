from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from company.models import Company, CustomUser, Staff, Employee


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(), message="This email already used"
            )
        ],
    )
    username = serializers.CharField(
        write_only=True,
        required=True,
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_verification = serializers.CharField(write_only=True, required=True)

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
            is_company=True,
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class CompanyRegistrationSerializer(CustomUserRegistrationSerializer):
    company_name = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            UniqueValidator(
                queryset=Company.objects.all(),
                message="Company with this name already exists",
            )
        ],
    )

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "password",
            "password_verification",
            "company_name",
        )


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        validators=[
            validate_password,
        ]
    )


class StaffRegistrationSerializer(CustomUserRegistrationSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "password",
            "password_verification",
        )


class StaffSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    company = serializers.SlugRelatedField(slug_field="company_name", read_only=True)

    class Meta:
        model = Staff
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
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
            name_values = Employee.objects.filter(
                company__company_user=user
            ).values_list("name", flat=True)
        else:
            company = user.company
            name_values = Employee.objects.filter(company=company).values_list(
                "name", flat=True
            )

        if validated_data["name"] in name_values:
            raise serializers.ValidationError({"name": "This employee already exists."})

        employee = Employee.objects.create(
            company=Company.objects.get(company_user=user), name=validated_data["name"]
        )
        employee.save()

        return employee

    class Meta:
        model = Employee
        fields = ("name",)
