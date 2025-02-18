from django.shortcuts import render
from rest_framework.response import Response
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



class CategoryListView(ListModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    
class CategoryDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

    def get(self,request, *args, **kwargs):
        return self.retrieve(request, *args,**kwargs)
    
class CategoryImageListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer

    def get_queryset(self):
        category_id = self.kwargs["category_id"]

        return self.queryset.filter(category=category_id)
    
    def get(self,request, *args, **kwargs):
        return self.list(request, *args,**kwargs)
    
    def post(self,request, *args, **kwargs):
        return self.create(request, *args,**kwargs)
