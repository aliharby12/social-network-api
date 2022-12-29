from post.serializer import PostSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from post.models import Post, UserLikedPost
from django.db.models.query import QuerySet


class PostListView(generics.ListAPIView):
    """
    list all posts data
    """

    serializer_class = PostSerializer

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.all().select_related("user").order_by("-created_at")


class AddPostView(generics.GenericAPIView):
    """
    create a new post instance
    """

    serializer_class = PostSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPostView(generics.GenericAPIView):
    """
    get a post data
    """

    serializer_class = PostSerializer

    def get(self, request: Request, uuid) -> Response:
        try:
            post = Post.objects.get(uuid=uuid)
        except:
            return Response(
                "no available posts with this uuid!", status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data)


class UpdatePostView(generics.GenericAPIView):
    """
    update a post data
    """

    serializer_class = PostSerializer

    def patch(self, request: Request, uuid) -> Response:
        post = Post.objects.get(uuid=uuid, user=request.user)
        serializer = PostSerializer(
            post, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePostView(generics.GenericAPIView):
    """
    delete a post data
    """

    serializer_class = PostSerializer

    def delete(self, request: Request, uuid) -> Response:
        try:
            post = Post.objects.get(uuid=uuid, user=request.user)
        except Post.DoesNotExist:
            return Response("Post not found!", status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response("deleted!", status=status.HTTP_204_NO_CONTENT)
