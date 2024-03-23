import shutil
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from posts.models import *
from uploads.models import ImageUpload

from .views import *

TEST_DIR = "test_images"

class UserTests(APITestCase):
    def test_list_user(self):
        """
        Ensure we get the list of users
        """
        url = reverse(CreateUserView.name)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """
        Ensure we can create a user
        """
        url = reverse(CreateUserView.name)
        data = {'username': 'test', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        list_response = self.client.get(url, format='json')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.json()['count'], 1)

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


class UserCreateMixin:

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser')
        user.set_password("testpassword")
        user.save()
        token = Token.objects.create(user=user)
        cls.user = user
        cls.token = token.key


class PostTests(UserCreateMixin, APITestCase):
    def setUp(self):
        self.client = APIClient()
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


    def test_post_detail_post_delete(self):
        """
            Ensure we can delete created posts
        """
        create_response = self.client.post(self.create_url, self.post_payload, format='multipart')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_data = create_response.data

        detail_url = reverse(PostDetail.name, kwargs={"slug": post_data['slug']})
        detail_response = self.client.delete(detail_url, format='json')
        self.assertEqual(detail_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.filter(slug=post_data['slug']).count(), 0)


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


class ImageUploadTests(UserCreateMixin, APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.uploads_url = reverse(UploadImageView.name)

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_image_upload(self):
        image_data = BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(image_data, format='png')
        image_data.seek(0)

        image_file = SimpleUploadedFile("test.png", image_data.read(), content_type='image/png')
        payload = {
            "name": "test_image",
            "image": image_file
        }
        upload_response = self.client.post(self.uploads_url, payload, format="multipart")
        self.assertEqual(upload_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ImageUpload.objects.filter(name=payload['name']).count(), 1)

        list_response = self.client.get(self.uploads_url, format='json')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        list_response_data = list_response.json()
        self.assertEqual(list_response_data['count'], 1)

    def test_image_upload_list(self):
        response = self.client.get(self.uploads_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryTests(UserCreateMixin, APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.category_url = reverse(CategoryListView.name)
        self.payload = {
            "name": "Test Category",
            "slug": "test-category"
        }

    def create_category(self):
        return self.client.post(self.category_url, self.payload, format='json')

    def test_category_list(self):
        response = self.client.get(self.category_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create(self):
        create_response = self.create_category()
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(name=self.payload['name']).count(), 1)

        list_response = self.client.get(self.category_url, format='json')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.json()['count'], 1)

    def test_category_detail_read(self):
        create_response = self.create_category()
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(name=self.payload['name']).count(), 1)

        detail_url = reverse(CategoryDetailView.name, kwargs={"slug": self.payload['slug']})
        detail_response = self.client.get(detail_url, format='json')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.json()['slug'], self.payload['slug'])

    def test_category_detail_patch_update(self):
        create_response = self.create_category()
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(name=self.payload['name']).count(), 1)

        detail_url = reverse(CategoryDetailView.name, kwargs={"slug": self.payload['slug']})
        update_payload = {"name": "updated category"}
        detail_response = self.client.patch(detail_url, update_payload, format='json')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.json()['name'], update_payload['name'])


class AuthorTests(UserCreateMixin, APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.author_url = reverse(AuthorList.name)
        self.payload = {
            "display_name": "Author Name",
            "short_description": "Backend Engineer who loves Python",
            "bio": "I like to travel in trains"
        }

    def test_author_list(self):
        response = self.client.get(self.author_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)

    def test_author_get(self):
        author = Author.objects.first()
        author_url = reverse(AuthorDetail.name, kwargs={"uuid": author.uuid})
        response = self.client.get(author_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['user'], author.user.username)

    def test_author_update(self):
        author = Author.objects.first()
        author_url = reverse(AuthorDetail.name, kwargs={"uuid": author.uuid})
        update_response = self.client.put(author_url, self.payload, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        updated_obj = Author.objects.get(uuid=author.uuid)
        self.assertEqual(updated_obj.display_name, self.payload['display_name'])
        self.assertEqual(updated_obj.short_description, self.payload['short_description'])
        self.assertEqual(updated_obj.bio, self.payload['bio'])

    def test_author_patch_update(self):
        author = Author.objects.first()
        author_url = reverse(AuthorDetail.name, kwargs={"uuid": author.uuid})
        patch_response = self.client.patch(author_url, {"bio": self.payload['bio']}, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        updated_obj = Author.objects.get(uuid=author.uuid)
        self.assertEqual(updated_obj.bio, self.payload['bio'])
