from django.urls import path
from categories.views import (CategoryViewSet, CategoryDetailViewSet,
                              CategoryImageViewSet)

from rest_framework_nested import routers

from django.urls import include

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)


catgories_router = routers.NestedDefaultRouter(
    router,
    "categories",
    lookup = "category"
)
catgories_router.register("category-detail",CategoryDetailViewSet)
catgories_router.register("category-images", CategoryImageViewSet)



urlpatterns = [
    path("", include(router.urls)),
    path("", include(catgories_router.urls)),
    # path("categories/", CategoryListView.as_view(), name="categories-list"),
    
    # path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    
    # path("categories/<int:category_id>/images/", CategoryImageListView.as_view(), name="category-images"),
]