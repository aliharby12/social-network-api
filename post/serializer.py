from rest_framework import serializers
from post.models import Post, UserLikedPost


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ["uuid", "title", "body", "likes_count", "created_at", "updated_at"]

    def get_likes_count(self, instance) -> int:
        return (
            UserLikedPost.objects.filter(post=instance)
            .select_related("post", "user")
            .count()
        )
