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
from rest_framework.generics import ListAPIView , ListCreateAPIView 
from rest_framework.viewsets import ModelViewSet , GenericViewSet

            
class ProductViewSet(ListModelMixin , CreateModelMixin ,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin,GenericViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(GenericViewSet, ListModelMixin , CreateModelMixin ,
                    RetrieveModelMixin, UpdateModelMixin,
                    DestroyModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs["product_pk"])
        
class FavoriteProdcutViewSet(RetrieveModelMixin,ListModelMixin ,
                              CreateModelMixin,DestroyModelMixin,
                              GenericViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    

    
class CartViewSet(ListModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset


class ProductTagViewSet(ListModelMixin,GenericViewSet):

    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]
    
class ProductImageViewSet(RetrieveModelMixin,ListModelMixin ,
                           CreateModelMixin,DestroyModelMixin,
                           GenericViewSet):
    queryset = ProductsImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
      return self.queryset.filter(product__id = self.kwargs["product_pk"])
    
