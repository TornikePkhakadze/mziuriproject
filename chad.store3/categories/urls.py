from django.urls import path
from categories.views import Cate


urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories")
    path("categories/<int:pk>/", CategoryDetail)
]