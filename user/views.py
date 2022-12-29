from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from post.serializer import PostSerializer, UserLikedPostsSerializer
from user.models import User
from typing import cast
from user.serializer import (
    CreateUserSerializer,
    UserSerializer,
    CreateUserSerializerResponse,
)
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.db.models.query import QuerySet
from post.models import Post, UserLikedPost


class UserCreateView(generics.GenericAPIView):
    """
    create a new user instance
    """
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: CreateUserSerializerResponse,
        }
    )
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(serializer.instance)

        return Response(
            {
                "access": str(token.access_token),
                "refresh": str(token),
                "user": UserSerializer(
                    instance=user, context={"request": request}
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileAPIView(generics.GenericAPIView):
    """
    get user profile data
    """
    serializer_class = UserSerializer

    def get(self, request) -> Response:
        try:
            user = User.objects.get(uuid=request.user.uuid)
        except:
            return Response("Unauthorized!", status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LikedPostsAPIView(generics.ListAPIView):
    """
    list user liked posts
    """
    serializer_class = UserLikedPostsSerializer

    def get_queryset(self) -> QuerySet[Post]:
        return UserLikedPost.objects.filter(user=self.request.user).select_related("user").order_by("-created_at")
