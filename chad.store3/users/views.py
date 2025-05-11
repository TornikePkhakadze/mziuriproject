from django.shortcuts import render
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from users.serializer import UserSerializer, RegisterSerializer, PasswordRestSerializer, PasswordResetConfirmSerializer
from rest_framework.decorators import action
from rest_framework import response, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import random
from users.models import EmailVerificationCode
from django.utils import timezone
from .serializer import EmailCodeConfirmSerializer

from datetime import timedelta
from config.celery import app


User = get_user_model()


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class CreateUser(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def perform_update(self, serializer):
        password = self.request.data.get('password', None)
        if password:
            self.request.user.set_password(password)
            self.request.user.save()
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class RestPasswordViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = PasswordRestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "მომხმარებელი ვერ მოიძებნა"}, status=status.HTTP_404_NOT_FOUND)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"http://127.0.0.1:8000/rest_password_confirm/{uid}/{token}"

            subject = "პაროლის აღდგენა"
            message = f"დააჭირეთ ლისნკის რათა აღადგინოთ პაროლი{reset_url}"

            app.send_task("users.tasks.send_mail_async", args=[subject,message,user.email])

            return Response({"message": "წერილი წარმატებით არის გაგზავნილი"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = PasswordResetConfirmSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uidb64', openapi.IN_PATH, description="User ID (Base64 encoded)", type=openapi.TYPE_STRING),
            openapi.Parameter("token", openapi.IN_PATH, description="Password reset token", type=openapi.TYPE_STRING),
        ]
    )
    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "პაროლი წარმატებით შეიცვალა"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class RegisterViewSet(CreateModelMixin,GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.send_verification_code(user)
            user = serializer.save()
        return Response(
            {"detail": "user registered succesfully. verification code sent to email"},
            status=status.HTTP_201_CREATED)
                                                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_code(self, user):
        code = str(random.randint(100000, 999999))

        EmailVerificationCode.objects.update_or_create(
            user=user,
            defaults={"code":code, "created_at": timezone.now()}
        )
        subject = "your verification"
        message = f"Hello {user.username}, your verification code is {code}"
        # send_mail(subject, message, 'no-reply@example.com', [user.email])
        app.send_task("users.tasks.send_mail_async", args=[subject,message,user.email])
    @action(detail=False, methods=["post"], url_path="resend_code", serializer_class = EmailVerificationCode)
    def resend_code(self,requset):
        serializer = self.serializer_class(data=requset.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data["user"]
        existing = EmailVerificationCode.objects.filter(user=user).first
        if existing:
            time_diff = timezone.now() - existing.created_at
            if time_diff < timedelta (minutes= 1):
                wait_seaconds = 60 - int(time_diff.total_seaconds())
                return Response(
                    {"detail" f"please wait {wait_seaconds} seaconds before trying again"},
                    status= 429
                )
        self.send_verification_code(user)
        return Response({"detail": "verification code resent"})    
    
    @action (detail=False, methods=["post"], url_path="confirm_code", serializer_class=EmailCodeConfirmSerializer)
    def  confirm_code(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            user.is_active = True
            user.save()
            return Response({"message": "momxmarebeli warmatebit aris gaaqtiurebuli"}, status=status.HTTP_200_OK )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
