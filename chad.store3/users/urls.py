from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, CreateUser, RestPasswordViewSet, PasswordResetConfirmViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("createuser", CreateUser, basename="createuser")
router.register("profile", UserViewSet, basename="profile")
router.register("reset_password", RestPasswordViewSet, basename="rest_password")

urlpatterns = [
    path("password_rest_confirm/<uidb64>/<token>/", PasswordResetConfirmViewSet.as_view({'post': 'create'}), name="password_reset_confirm"),
    path("", include(router.urls)), 
]
