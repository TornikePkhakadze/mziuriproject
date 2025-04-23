from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import EmailVerificationCode

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "first_name", "last_name"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required = True, write_only= True, validators=[validate_password])
    password2 = serializers.CharField(required = True, write_only= True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "first_name", "last_name", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "passwords don't match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save
        return user
    
class PasswordRestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self,value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("ver vipove mag emailit user i")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only= True, required= True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required = True)

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'passwords dont match'})
        
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uidb64"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({"message": 'momxmarebeli ver moidzebna'}) 


        token = attrs["token"]
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"message": 'arasworian vadagasuli ari tokeni'})

        attrs['user'] = user
        return attrs
    
    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password"])
        user.save()


class EmailCodeResendSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        email  = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "მომხმარებელი ვერ მოიძებნა"})
        attrs["user"] = user
        return attrs
    
class EmailCodeConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self,attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
            verification = EmailVerificationCode.objects.filter(user=user).first()

            if not verification.code == code:
                raise serializers.ValidationError({"message":"kodi arasworia"})
            
            if verification.is_expiered():
                raise serializers.ValidationError({"message": "kodi vadagasulia"})
        except (User.DoesNotExist, EmailVerificationCode.DoesNotExist):
                raise serializers.ValidationError({"message": "momxmarebeli an amasan dakavshirebuli kodi ar moidzebna"})
        
        attrs["user"] = user
        return attrs


