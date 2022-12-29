from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase

from post.models import Post
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User


class TestCreatePost(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("post:add-post")
        self.user = User.objects.create(
            name="test user", email="test@test.test", gender="M"
        )
        self.user.set_password("test@1234")
        self.user.save()
        self.token = RefreshToken.for_user(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token.access_token}"}
        self.body = {
            "title": "test title",
            "body": "test body",
        }
        self.body_no_title = {
            "body": "test body",
        }
        self.body_no_body = {
            "title": "test title",
        }
        self.body_no_token = {
            "title": "test title",
            "body": "test body",
        }

        super().setUp()

    def test_create_post_successfully(self):
        response = self.client.post(
            self.url, data=self.body, format="json", **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_fail_no_title(self):
        response = self.client.post(
            self.url, data=self.body_no_title, format="json", **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["title"][0]), "This field is required.")

    def test_create_post_fail_no_body(self):
        response = self.client.post(
            self.url, data=self.body_no_body, format="json", **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["body"][0]), "This field is required.")

    def test_create_post_fail_no_token(self):
        response = self.client.post(self.url, data=self.body_no_token, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestGetPosts(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name="test user", email="test@test.test", gender="M"
        )
        self.user.set_password("test@1234")
        self.user.save()
        self.token = RefreshToken.for_user(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token.access_token}"}
        self.posts = Post.objects.bulk_create(
            [
                Post(user=self.user, title="test title", body="test body"),
                Post(user=self.user, title="test title2", body="test body2"),
                Post(user=self.user, title="test title22", body="test body22"),
            ]
        )
        self.first_post = Post.objects.first()
        self.list_all_posts_url = reverse("post:all-posts")
        self.get_post_url = reverse(
            "post:get-post", kwargs={"uuid": self.first_post.uuid}
        )
        self.get_post_wrong_uuid_url = reverse(
            "post:get-post", kwargs={"uuid": self.user.uuid}
        )
        self.token = RefreshToken.for_user(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token.access_token}"}

    def test_list_all_posts_successfully(self):
        response = self.client.get(
            self.list_all_posts_url, format="json", **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_all_posts_no_token(self):
        response = self.client.get(self.list_all_posts_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_post_successfully(self):
        response = self.client.get(self.get_post_url, format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_wrong_uuid(self):
        response = self.client.get(
            self.get_post_wrong_uuid_url, format="json", **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_no_token(self):
        response = self.client.get(self.get_post_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUpdateDeletePost(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name="test user", email="test@test.test", gender="M"
        )
        self.user.set_password("test@1234")
        self.user.save()
        self.token = RefreshToken.for_user(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token.access_token}"}
        self.post = Post.objects.create(
            user=self.user, title="test title", body="test body"
        )
        self.update_url = reverse("post:update-post", kwargs={"uuid": self.post.uuid})
        self.update_url_wrong_uuid = reverse(
            "post:update-post", kwargs={"uuid": self.user.uuid}
        )
        self.delete_url = reverse("post:delete-post", kwargs={"uuid": self.post.uuid})
        self.delete_url_wrong_uuid = reverse(
            "post:delete-post", kwargs={"uuid": self.user.uuid}
        )

    def test_update_post_successfully(self):
        response = self.client.patch(self.update_url, {}, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_wrong_uuid(self):
        response = self.client.patch(self.update_url_wrong_uuid, {}, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_no_token(self):
        response = self.client.patch(self.update_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_successfully(self):
        response = self.client.delete(self.delete_url, {}, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_wrong_uuid(self):
        response = self.client.delete(self.delete_url_wrong_uuid, {}, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_no_token(self):
        response = self.client.delete(self.delete_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestLikeUnlikePost(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name="test user", email="test@test.test", gender="M"
        )
        self.user.set_password("test@1234")
        self.user.save()
        self.token = RefreshToken.for_user(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token.access_token}"}
        self.post = Post.objects.create(
            user=self.user, title="test title", body="test body"
        )
        self.like_unlike_post_url = reverse(
            "post:like-unlike-post", kwargs={"uuid": self.post.uuid}
        )

    def test_like_post_successfully(self):
        response = self.client.post(self.like_unlike_post_url, {}, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_post_successfully(self):
        response = self.client.post(self.like_unlike_post_url, {}, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_post_no_token(self):
        response = self.client.post(self.like_unlike_post_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
