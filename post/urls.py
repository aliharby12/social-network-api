from django.urls import path

from post.views import *

app_name = "post"
urlpatterns = [
    path("user-posts/", PostListView.as_view(), name="user-posts"),
    path("get-post/<uuid:uuid>/", GetPostView.as_view(), name="get-post"),
    path("add-posts/", AddPostView.as_view(), name="add-post"),
    path("update-post/<uuid:uuid>/", UpdatePostView.as_view(), name="update-post"),
    path("delete-post/<uuid:uuid>/", DeletePostView.as_view(), name="delete-post"),
]
