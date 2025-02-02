from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Review, Cart, ProductTag, FavoriteProduct
from .serializer import ReviewSerializer, CartSerializer
from users.models import User

@api_view(['GET', 'POST'])
def product_view(request):
    if request.method == 'GET':
        products = Product.objects.all()  
        product_list = []

        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'currency': product.currency,
            }
            product_list.append(product_data)
        return Response(product_list) 

    elif request.method == 'POST':
        data = request.data
        try:
            new_product = Product.objects.create(
                name=data.get('name'),
                description=data.get('description'),
                price=data.get('price'),
                currency=data.get('currency', 'GEL')
            )
            return Response({'id': new_product.id}, status=status.HTTP_201_CREATED) 

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(["GET", "POST"])
def review_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        review_list = []

        for review in reviews:
            review_data = {
                'id': review.id,
                'product_id': review.product.id,  
                'content': review.content,
                'rating': review.rating
            }
            review_list.append(review_data)

        return Response({'reviews': review_list})
    
    elif request.method == "POST":
        serializer = ReviewSerializer(data=request.data, context={"request": request})  
        if serializer.is_valid():
            review = serializer.save()
            return Response(
                {'id': review.id, 'message': 'Review created successfully!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
        serializer = CartSerializer(data=request.data, context={"request": request})
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

