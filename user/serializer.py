from rest_framework import serializers
from django.contrib.auth import get_user_model
from post.models import Post


class UserSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "gender", "posts_count"]

    def get_posts_count(self, instance) -> int:
        return Post.objects.filter(user=instance).select_related("user").count()


class CreateUserSerializerResponse(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "name", "gender", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it
        """
        return get_user_model().objects.create_user(**validated_data)
