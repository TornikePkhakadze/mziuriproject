from django.urls import path
from products.views import (ProductViewSet,ReviewViewSet,
                               FavoriteProdcutViewSet, CartViewSet,
                               ProductTagListView,ProductImageViewSet)

urlpatterns = [
    path('products/', ProductViewSet.as_view(), name="products"),
    path('reviews/', ReviewViewSet.as_view(), name='reviews'),
    path("products/<int:pk>/", ProductViewSet.as_view(), name="product" ),
    path("favorite_products/", FavoriteProdcutViewSet.as_view(), name="favorie_products"),
    path("favorite_products/<int:pk>/", FavoriteProdcutViewSet.as_view(), name="favorie_products"),
    path("cart/", CartViewSet.as_view(), name = "cart"),
    path("tags/", ProductTagListView.as_view(), name= "tags"),
    path("products/<int:product_id>/images/", ProductImageViewSet.as_view(), name="images"),
    path("products/<int:product_id>/images/<int:pk>/", ProductImageViewSet.as_view(), name="image"),
]