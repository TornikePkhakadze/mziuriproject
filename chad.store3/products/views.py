from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Review, Cart, ProductTag, FavoriteProduct
from .serializer import ReviewSerializer, CartModelSerializer, ProductSerializer, FavoriteProductSerializer, CartSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView  
from django.shortcuts import get_object_or_404
from rest_framework.mixins import (ListModelMixin , CreateModelMixin ,
                                   RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin,)

class ProductViewSet(ListModelMixin,GenericAPIView,
                     CreateModelMixin,RetrieveModelMixin,
                     UpdateModelMixin,DestroyModelMixin
                     ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request,pk=None, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk :
           return self.retrieve(request,*args,**kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args,**kwargs)
    
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
        


@api_view(["GET", "POST"])
def cart_view(request):
    if request.method == 'GET':
        carts = Cart.objects.all()
        cart_list = []

        for cart in carts:
            cart_data = {
                "id": cart.id,
                "products": list(cart.products.values("id", "name", "price")),
            }
            cart_list.append(cart_data)

        return Response({'carts': cart_list})

    elif request.method == 'POST':
        serializer = CartModelSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            cart = serializer.save()
            return Response(
                {'id': cart.id, 'message': 'Product added to cart successfully!'},
                status=status.HTTP_201_CREATED
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
def product_tag_view(request):
    if request.method == 'GET':
        tags = ProductTag.objects.all()
        tag_list = []

        for tag in tags:
            tag_data = {
                'name': tag.name,
                "products": list(tag.products.values("id", "name")),

            }
            tag_list.append(tag_data)

        return Response({'tags': tag_list})
    
    elif request.method == 'POST':
        serializer = ProductTag(data=request.data, context={"request": request})
        if serializer.is_valid():
            tag = serializer.save()
            return Response(
                {'id': tag.id, 'message': 'tag added to product successfully!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET","POST"])
def favorite_product_view(request):
    if request.method == 'GET':
        favorite = FavoriteProduct.objects.all()
        favo_list = []

        for favos in favorite:
            favo_data = {
                "products": list(favorite.products.values("id", "name")),
                'user': favos.user
            }
            favo_list.append(favo_data)

            return Response({'favorite': favo_list})
        
    elif request.method == 'POST':
        serializer = ProductTag(data=request.data, context={"request": request})
        if serializer.is_valid():
            favo = serializer.save()
            return Response(
                {'id': favo.id, 'message': 'favorite product added successfully!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
