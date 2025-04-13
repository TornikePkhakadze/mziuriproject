from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, CreateUser, RestPasswordViewSet, PasswordRestConfiemViewSet



router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("createuser", CreateUser, basename="createuser")
router.register(r'profile', UserViewSet, basename='profile')
router.register('reset_password', RestPasswordViewSet, basename="rest_password")
urlpatterns = [
    path("password_rest_confirm/<uidb64>/<token>/",PasswordRestConfiemViewSet.as_view({'post':'create'}), name= "passsword_reset_confirm"),  include(router.urls),
    path('users/', include(router.urls)),
]