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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .paginationfile import ProductPagination 
from .filters import ProductFilter,ReviewFilter
from rest_framework.exceptions import PermissionDenied

class ProductViewSet(ListModelMixin , CreateModelMixin ,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin,GenericViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    # filterset_fields = ["categories", "price"]
    filterset_class = ProductFilter

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "description"]
    pagination_class = ProductPagination



class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["rating_max", "rating_min"]
    filterset_class = ReviewFilter

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs["product_pk"])
        
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("you are not allowed to delete his review")
        instance.delete()

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("you cant change this review")
        serializer.save()

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
    
