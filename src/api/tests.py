from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from posts.models import *

from .views import *


class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a user
        """
        url = reverse(CreateUserView.name)
        data = {'username': 'test', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtain_token(self):
        """
        Ensure we can obtain auth token
        """
        user_url = reverse(CreateUserView.name)
        data = {'username': 'test', 'password': 'testpass'}
        user_response = self.client.post(user_url, data, format='json')
        self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)

        token_url = reverse('obtain-token')
        token_response = self.client.post(token_url, data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)


class PostTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_url = reverse(CreateUserView.name)
        data = {'username': 'test', 'password': 'testpass'}
        user_response = self.client.post(user_url, data, format='json')

        token_url = reverse('obtain-token')
        token_response = self.client.post(token_url, data, format='json')

        self.token = token_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.post_payload = {
            "title": "Test Post",
            "overview": "Overview of the post",
            "content": "This is the content of the post. Extra long sentence",
            "slug": "test-post"
        }
        self.create_url = reverse(PostCreateList.name)

    def test_post_list(self):
        """
            Ensure we can check posts list
        """
        list_response = self.client.get(self.create_url, format='json')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

    def test_post_create(self):
        """
            Ensure we can create posts
        """
        response = self.client.post(self.create_url, self.post_payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_query = Post.objects.filter(slug="test-post")
        self.assertEqual(post_query.count(), 1)

    def test_post_detail_read(self):
        """
            Ensure we can retrieve created posts
        """
        create_response = self.client.post(self.create_url, self.post_payload, format='multipart')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_data = create_response.data

        detail_url = reverse(PostDetail.name, kwargs={"slug": post_data['slug']})
        detail_response = self.client.get(detail_url, format='json')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

    def test_post_detail_patch_update(self):
        """
            Ensure we can patch update created posts
        """
        create_response = self.client.post(self.create_url, self.post_payload, format='multipart')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_data = create_response.data

        detail_url = reverse(PostDetail.name, kwargs={"slug": post_data['slug']})
        patch_payload = {"title": "updated title"}
        detail_response = self.client.patch(detail_url, patch_payload, format='json')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['title'], patch_payload['title'])

    def test_post_detail_post_update(self):
        """
            Ensure we can post update created posts
        """
        create_response = self.client.post(self.create_url, self.post_payload, format='multipart')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_data = create_response.data

        detail_url = reverse(PostDetail.name, kwargs={"slug": post_data['slug']})
        post_payload = {"title": "updated title", "slug": "updated-title"}
        detail_response = self.client.patch(detail_url, post_payload, format='json')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['title'], post_payload['title'])
        self.assertEqual(detail_response.data['slug'], post_payload['slug'])


class PostPermissionTests(APITestCase):
    def setUp(self):
        self.post_payload = {
            "title": "Test Post",
            "overview": "Overview of the post",
            "content": "This is the content of the post. Extra long sentence",
            "slug": "test-post"
        }
        self.create_url = reverse(PostCreateList.name)

    def test_post_list_permission(self):
        list_response = self.client.get(self.create_url, format='json')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

    def test_post_create_permission(self):
        create_response = self.client.post(self.create_url, self.post_payload, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
