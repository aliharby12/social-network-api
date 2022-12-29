from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import *

app_name = "user"
urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("liked-posts/", LikedPostsAPIView.as_view(), name="liked-posts"),
    path("my-posts/", MyPostsAPIView.as_view(), name="my-posts"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
