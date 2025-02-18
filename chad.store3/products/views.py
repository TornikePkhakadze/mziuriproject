from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Review, Cart, ProductTag, FavoriteProduct, ProductsImage
from .serializer import (ReviewSerializer, CartModelSerializer,
                        ProductSerializer, FavoriteProductSerializer, 
                        CartSerializer,ProductTagSerializer,
                        ProductImageSerializer)
from users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView  
from django.shortcuts import get_object_or_404
from rest_framework.mixins import (ListModelMixin , CreateModelMixin ,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin,)

class ProductViewSet(ListModelMixin, GenericAPIView,
                         CreateModelMixin, RetrieveModelMixin,
                           UpdateModelMixin, DestroyModelMixin):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ReviewViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        

class FavoriteProdcutViewSet(ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin, GenericAPIView):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    def get(self,request,pk=None,*args,**kwargs):
        if pk:
            return self.retrieve(request,*args,**kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request, *args,**kwargs)
    
class CartViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductTagListView(ListModelMixin, GenericAPIView, CreateModelMixin):

    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ProductImageViewSet(ListModelMixin, CreateModelMixin,
                           DestroyModelMixin, RetrieveModelMixin,
                             GenericAPIView):
    queryset = ProductsImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
      return self.queryset.filter(product__id = self.kwargs["product_id"])
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request, *args,**kwargs)