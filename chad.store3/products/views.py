from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Review, Cart, ProductTag, FavoriteProduct, ProductsImage, CartItem
from .serializer import (ReviewSerializer, CartModelSerializer,
                        ProductSerializer, FavoriteProductSerializer, 
                        CartItemSerializer,ProductTagSerializer,
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
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.decorators import action
from .permissions import IsObjectOwnerOrReadOnly
    


class ProductViewSet(ListModelMixin , CreateModelMixin ,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin,GenericViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    # filterset_fields = ["categories", "price"]
    filterset_class = ProductFilter
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    throttle_scope = 'likes'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "description"]
    pagination_class = ProductPagination

    @action(detail=False, methods=["GET"], url_path="my_products")
    def my_products(self, request, pk=None):
        queryset = self.queryset.filter(user=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["rating_max", "rating_min"]
    filterset_class = ReviewFilter

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs["product_pk"])
        
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("you are not allowed to delete his review")
        instance.delete()

    # def perform_update(self, serializer):
    #     obj = self.get_object()
    #     if obj.user != self.request.user:
    #         raise PermissionDenied("you cant change this review")
    #     serializer.save()

class FavoriteProdcutViewSet(RetrieveModelMixin,ListModelMixin ,
                              CreateModelMixin,DestroyModelMixin,
                              GenericViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    

    
class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    
    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied("you are not allowed to delete this cart")
        instance.delete()

    # def perform_update(self, serializer):
    #     instance = self.get_object()
    #     if instance.cart.user != self.request.user:
    #         raise PermissionDenied("you cant change this item")
    #     serializer.save()





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
    
