from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, CreateUser

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("createuser", CreateUser, basename="createuser")
router.register(r'profile', UserViewSet, basename='profile')

urlpatterns = [
    path("", include(router.urls)),
    path('users/', include(router.urls)),
]