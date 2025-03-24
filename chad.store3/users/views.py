from django.shortcuts import render
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin , DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from users.serializer import UserSerializer, RegisterSerializer
from rest_framework.decorators import action

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
        return self.request.user.user

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user.ser
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def perform_update(self, serializer):
        password = self.request.data.get('password', None)
        if password:
            self.request.user.set_password(password)
            self.request.user.save()
        serializer.save()

    def perform_destroy(self, instance):
        instance.user.delete()