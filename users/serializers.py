from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password must be atleast 8 characters.",
        },
        allow_blank=False,
        required=True
    )

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
            queryset= CustomUser.objects.all(),
            message="This email is already registered with us.",
        )],
        error_messages={
            "required": "Email field is required.",
            "invalid" : "Kindly enter a Valid Email Address",
        },
        allow_blank=False,
        required=True
    )

    first_name = serializers.CharField(
        allow_blank=False,
        required=True,
        error_messages={
            "required": "Name field is required.",
        },)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'contact', 'password']

    def save(self, otp):

        user = CustomUser.objects.create_user(
            email=self.validated_data['email'],
            username=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            password=self.validated_data['password'],
            contact=self.validated_data['contact'],
            otp= otp
        )

        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)

class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['otp']

class ForgetPasswordSerializer(serializers.Serializer):
    '''This serializer takes input for POST request to generate OTP i.e.
    required to change the password using email address of user.'''

    email = serializers.EmailField(
        error_messages={
            "required": "Email field is required.",
            "invalid" : "Kindly enter a Valid Email Address",
        },
        allow_blank=False,
        required=True
    )

class ChangePasswordSerializer(serializers.Serializer):
    '''This serialiser takes input for POST request to change
    user password with OTP, Email and New Password'''

    email = serializers.EmailField(
        error_messages={
            "required": "Email field is required.",
            "invalid" : "Kindly enter a Valid Email Address",
        },
        allow_blank=False,
        required=True
    )
    otp = serializers.CharField(
        error_messages={
            "required": "OTP field is required.",
        },
        allow_blank=False,
        required=True
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password must be atleast 8 characters.",
        },
        allow_blank=False,
        required=True
    )

class ChangeMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']

class CheckOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            "required": "Email field is required.",
            "invalid" : "Enter a valid email address."
        },
        allow_blank=False,
        required=True
    )
    otp = serializers.CharField(
        error_messages={
            "required": "OTP field is required.",
            "invalid": "Ensure this field has no more than 4 characters."
        },
        max_length=4,
        min_length=4,
        allow_blank=False,
        required=True
    )
