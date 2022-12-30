from unittest import skip
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase

from user.models import User
from post.models import Post, UserLikedPost
from rest_framework_simplejwt.tokens import RefreshToken


class TestCreateUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("user:register")
        self.body = {
            "email": "test@test.test",
            "name": "test user",
            "gender": "M",
            "password": "test@1234",
        }
        self.body_no_email = {
            "name": "test user",
            "gender": "M",
            "password": "test@1234",
        }
        self.body_no_name = {
            "email": "test@test.test",
            "gender": "M",
            "password": "test@1234",
        }
        self.body_no_password = {
            "email": "test@test.test",
            "name": "test user",
            "gender": "M",
        }

        super().setUp()

    @skip
    def test_create_user_successfully(self):
        response = self.client.post(self.url, data=self.body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_fail_no_email(self):
        response = self.client.post(self.url, data=self.body_no_email, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["email"][0]), "This field is required.")

    def test_create_user_fail_no_name(self):
        response = self.client.post(self.url, data=self.body_no_name, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["name"][0]), "This field is required.")

    def test_create_user_fail_no_password(self):
        response = self.client.post(self.url, data=self.body_no_password, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["password"][0]),
            "This field is required.",
        )


class TestLoginAndProfile(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name="test user", email="test@test.test", gender="M"
        )
        self.user.set_password("test@1234")
        self.user.save()
        self.body = {"email": "test@test.test", "password": "test@1234"}
        self.body_wrong_password = {"email": "test@test.test", "password": "test1@1234"}
        self.body_wrong_email = {"email": "test12@test.test", "password": "test@1234"}
        self.login_url = reverse("user:login")
        self.profile_url = reverse("user:profile")
        self.token = RefreshToken.for_user(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token.access_token}"}

    def test_login_successfully(self):
        response = self.client.post(self.login_url, data=self.body, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_login_fail_wrong_password(self):
        response = self.client.post(
            self.login_url, data=self.body_wrong_password, format="json"
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_fail_wrong_email(self):
        response = self.client.post(
            self.login_url, data=self.body_wrong_email, format="json"
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_successfully(self):
        response = self.client.get(
            self.profile_url, data=self.body, format="json", **self.headers
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_profile_no_token(self):
        response = self.client.get(self.profile_url, data=self.body, format="json")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestGetMyPosts(TestCase):
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
        self.list_my_posts_url = reverse("user:my-posts")
        self.token = RefreshToken.for_user(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token.access_token}"}

    def test_list_my_posts_successfully(self):
        response = self.client.get(
            self.list_my_posts_url, format="json", **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_my_posts_no_token(self):
        response = self.client.get(self.list_my_posts_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestGetMyPosts(TestCase):
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
        self.liked_posts = UserLikedPost.objects.bulk_create(
            [
                UserLikedPost(user=self.user, post=Post.objects.first()),
                UserLikedPost(user=self.user, post=Post.objects.last()),
            ]
        )
        self.list_liked_posts_url = reverse("user:liked-posts")
        self.token = RefreshToken.for_user(self.user)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token.access_token}"}

    def test_list_liked_posts_successfully(self):
        response = self.client.get(
            self.list_liked_posts_url, format="json", **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_liked_posts_no_token(self):
        response = self.client.get(self.list_liked_posts_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
