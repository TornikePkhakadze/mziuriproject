from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Category, CategoryImage
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from rest_framework.mixins import (ListModelMixin , CreateModelMixin ,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin,)
from categories.serializers import CategorySerializer

from .serializers import (CategoryDetailSerializer,CategorySerializer,
                          CategoryImageSerializer)

from rest_framework.generics import ListAPIView , ListCreateAPIView
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser


class CategoryViewSet(GenericViewSet,ListModelMixin , CreateModelMixin ,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin,):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name",]
    parser_classes = [MultiPartParser, FormParser]

    
    
class CategoryDetailViewSet(GenericViewSet,ListModelMixin , CreateModelMixin ,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin,):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticated]


    
class CategoryImageViewSet(GenericViewSet,ListModelMixin , CreateModelMixin ,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin,):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs["category_id"]

        return self.queryset.filter(category=category_id)
