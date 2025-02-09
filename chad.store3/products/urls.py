from django.urls import path
from products.views import ProductViewSet,ReviewViewSet,cart_view, product_tag_view,favorite_product_view

urlpatterns = [
    path('products/', ProductViewSet.as_view(), name="products"),
    path('reviews/', ReviewViewSet.as_view(), name='reviews'),
    path('carts/', cart_view, name='carts'),
    path('tags/', product_tag_view, name='tags'),
    path("products/<int:pk>/", ProductViewSet.as_view(), name="product" ),

]