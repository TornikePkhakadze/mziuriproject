from django.urls import path
from products.views import (ProductViewSet,ReviewViewSet,
                               FavoriteProdcutViewSet, CartViewSet,
                               ProductTagListView,ProductImageViewSet)

urlpatterns = [
    path('products/', ProductViewSet.as_view({"get":"list", "post":"create"}), name="products"),
    # path('reviews/', ReviewViewSet.as_view(), name='reviews'),
    path("products/<int:product_id>/reviews/", ReviewViewSet.as_view(), name = 'reviews'),
    path("products/<int:pk>/", ProductViewSet.as_view({"get":"retrieve","post":"create",
                                                                      "put":"update","delete":"destroy",
                                                                      "patch":"partial_update"}), name="product" ),


    path("favorite_products/", FavoriteProdcutViewSet.as_view({"get":"list", "post":"create"}), name="favorie_products"),
    path("favorite_products/<int:pk>/", FavoriteProdcutViewSet.as_view({"get":"retrieve","delete":"destroy",
                                                                      }), name="favorie_products"),
    path("cart/", CartViewSet.as_view(), name = "cart"),
    path("tags/", ProductTagListView.as_view(), name= "tags"),
    path("products/<int:product_id>/images/", ProductImageViewSet.as_view({"get":"list", "post":"create"}), name="images"),
    path("products/<int:product_id>/images/<int:pk>/", ProductImageViewSet.as_view({"get":"retrieve","delete":"destroy",
                                                                      "put":"update","post":"create"}), name="image"),
]