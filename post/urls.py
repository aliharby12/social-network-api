from django.urls import path

from post.views import *

app_name = "post"
urlpatterns = [
    path("posts/", PostListView.as_view(), name="all-posts"),
    path("get-post/<uuid:uuid>/", GetPostView.as_view(), name="get-post"),
    path("add-post/", AddPostView.as_view(), name="add-post"),
    path("update-post/<uuid:uuid>/", UpdatePostView.as_view(), name="update-post"),
    path("delete-post/<uuid:uuid>/", DeletePostView.as_view(), name="delete-post"),
    path(
        "like-unlike-post/<uuid:uuid>/",
        LikeUnlikePostView.as_view(),
        name="like-unlike-post",
    ),
]
