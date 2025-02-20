from django.urls import path
from categories.views import (CategoryListView, CategoryDetailView,
                              CategoryImageListView)


urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("categories/<int:category_id>/images/", CategoryImageListView.as_view(), name="category-images"),
]