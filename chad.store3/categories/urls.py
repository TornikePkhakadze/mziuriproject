from django.urls import path
from categories.views import (CategoryListView, CategoryDetailView,
                              CategoryImageListView)


urlpatterns = [
    path("categories/", CategoryListView.as_view({"get":"list", "post":"create"}), name="categories-list"),
    
    path("categories/<int:pk>/", CategoryDetailView.as_view({"get":"retrieve","post":"create",
                                                                      "put":"update","delete":"destroy",
                                                                      "patch":"partial_update"}), name="category-detail"),
    
    path("categories/<int:category_id>/images/", CategoryImageListView.as_view({"get":"retrieve","delete":"destroy",
                                                                      "put":"update","post":"create"}), name="category-images"),
]