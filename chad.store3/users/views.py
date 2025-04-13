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

            send_mail(
                "პაროლის აღდგენა",
                f"დააჭირეთ ლინკს რათა აღადგინოთ პაროლი: {reset_url}",
                "ttttornikeeee@gmail.com",
                [user.email],
                fail_silently=False
            )

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
