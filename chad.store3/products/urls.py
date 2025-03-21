from django.urls import path
from products.views import (ProductViewSet,ReviewViewSet,
                               FavoriteProdcutViewSet, CartItemViewSet,
                               ProductTagViewSet,ProductImageViewSet,
                               )


from rest_framework_nested import routers

from django.urls import include

router = routers.DefaultRouter()
router.register("products", ProductViewSet)
router.register("favorite_products", FavoriteProdcutViewSet)
router.register("cart", CartItemViewSet)
router.register("tags",ProductTagViewSet)
router.register("cart_items", CartItemViewSet, basename="cart-items")

products_router = routers.NestedDefaultRouter(
    router,
    "products",
    lookup = "product",
)

products_router.register("images", ProductImageViewSet)
products_router.register("reviews",ReviewViewSet)
# products_router.register(r"my_products", ProductViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
    # path('reviews/', ReviewViewSet.as_view(), name='reviews'),
 
    # path("cart/", CartViewSet.as_view(), name = "cart"),
    # path("tags/", ProductTagListView.as_view(), name= "tags"),
#     path("products/<int:product_id>/images/", ProductImageViewSet.as_view({"get":"list", "post":"create"}), name="images"),
#     path("products/<int:product_id>/images/<int:pk>/", ProductImageViewSet.as_view({"get":"retrieve","delete":"destroy",
#                                                                       "put":"update","post":"create"}), name="image"),
 ]
