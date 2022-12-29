from django.db import models

from user.models import User


class TimeStampedModel(models.Model):
    """
    database model for created at and updated at fields
    """

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    """
    database table to save user posts
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    title = models.CharField(max_length=256)
    body = models.TextField()

    def get_likes_count(self) -> int:
        return UserLikedPost.objects.filter(post=self).select_related("post").count()

    def __str__(self) -> str:
        return f"{self.user.email} : {self.title}"


class UserLikedPost(TimeStampedModel):
    """
    database table to save user liked posts
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_posts")

    def __str__(self) -> str:
        return f"{self.user.email} liked {self.post.title}"
