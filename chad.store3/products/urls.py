from django.urls import path
from products.views import product_view,review_view,cart_view, product_tag_view,favorite_product_view

urlpatterns = [
    path('products/', product_view, name="products"),
    path('reviews/', review_view, name='reviews'),
    path('carts/', cart_view, name='carts'),
    path('tags/', product_tag_view, name='tags')

]