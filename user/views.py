from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from post.serializer import PostSerializer, UserLikedPostsSerializer
from user.models import User
from typing import cast
from user.tasks import save_holiday_for_user
from user.serializer import (
    CreateUserSerializer,
    UserSerializer,
    CreateUserSerializerResponse,
)
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.db.models.query import QuerySet
from post.models import Post, UserLikedPost
from django.db import transaction
import requests
from django.conf import settings


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
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        save_holiday_for_user.delay(user.id)
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

        # HINT:
        # I commented on this part of the code because Django
        # by default validates the email formatting
        # email = serializer.validated_data["email"]
        # e_response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={settings.EMAIL_KEY}&email={email}")
        # if e_response.json()["is_valid_format"]["value"] == True:
        #     user = serializer.save()
        #     save_holiday_for_user.delay(user.id)
        #     token = RefreshToken.for_user(serializer.instance)
        #     return Response(
        #         {
        #             "access": str(token.access_token),
        #             "refresh": str(token),
        #             "user": UserSerializer(
        #                 instance=user, context={"request": request}
        #             ).data,
        #         },
        #         status=status.HTTP_201_CREATED,
        #     )
        # return Response("enter a valid email address", status=status.HTTP_400_BAD_REQUEST)


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


class MyPostsAPIView(generics.ListAPIView):
    """
    list all my posts data
    """

    serializer_class = PostSerializer

    def get_queryset(self):
        return (
            Post.objects.filter(user=self.request.user)
            .select_related("user")
            .order_by("-created_at")
        )


class LikedPostsAPIView(generics.ListAPIView):
    """
    list user liked posts
    """

    serializer_class = UserLikedPostsSerializer

    def get_queryset(self) -> QuerySet[Post]:
        return (
            UserLikedPost.objects.filter(user=self.request.user)
            .select_related("user")
            .order_by("-created_at")
        )
