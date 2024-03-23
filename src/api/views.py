from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, permissions, serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api import custompermission
from posts import models
from uploads.models import ImageUpload

from . import serializers
from .serializers import (AuthorSerializer, CategorySerializer,
                          CreateUserSerializer, PostSerializer)


class PostCreateList(generics.ListCreateAPIView):
    """
    `GET` Retrieve a List of Blog Posts

    `GET` Retrieve Details for a Blog Post

    """
    queryset = models.Post.objects.select_related('author', 'category', 'featured_image').all()
    serializer_class = PostSerializer
    name = 'Posts List'
    lookup_field = 'slug'
    filter_fields = (
        'category__slug',
        'author__display_name',
        'is_published'
    )
    search_fields = (
        '$title',
    )
    ordering_fields = (
        'title',
        'published_date',
    )

    def perform_create(self, serializer):
        author = models.Author.objects.get(user=self.request.user)
        serializer.save(author=author)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    `PUT` Replace a Blog Post

    `PATCH` Update a Blog Post

    `DELETE` Delete a Blog Post

    """
    queryset = models.Post.objects.select_related('author', 'category', 'featured_image').all()
    serializer_class = PostSerializer
    name = 'post-detail'
    lookup_field = 'slug'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentUserAuthorOrReadOnly,
    )


class AuthorList(generics.ListAPIView):
    """
    `GET` Retrieve a List of Authors

    `GET` Retrieve Details for a Specific Author

    """
    name = 'author-list'
    queryset = models.Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'uuid'
    search_fields = (
        '$display_name',
    )
    ordering_fields = (
        'display_name',
    )


class AuthorDetail(generics.RetrieveUpdateAPIView):
    """
    `PUT` Replace an Author 

    `PATCH` Update an Author
    """
    name = "author-detail"
    queryset = models.Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'uuid'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentUserOwnerOrReadOnly,
    )


class CategoryListView(generics.ListCreateAPIView):
    """
    `GET` Retrieve a List of Categories

    `GET` Retrieve Details for a Specific Category

    `POST` Create a Category

    """
    name = 'category-list'
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class CategoryDetailView(generics.RetrieveUpdateAPIView):
    """
    `PUT` Replace a Category 

    `PATCH` Update a Category

    """
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    name = "category-detail"


class CreateUserView(generics.ListCreateAPIView):
    """
    `GET` Retrieve a list of Users

    `POST` Create a new User

    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    throttle_scope = 'register'
    name = 'Create User'
    permission_classes = (
        permissions.AllowAny,
    )


class UploadImageView(generics.ListCreateAPIView):
    """
    `GET` Retrieves a List of Uploaded Images

    `POST` Upload an image to the platform.

    """
    queryset = ImageUpload.objects.select_related('uploaded_by__author').all()
    throttle_scope = 'uploads'
    serializer_class = serializers.ImageUploadSerializer
    name = 'Image Uploads'

    filter_fields = (
        'uploaded_by',
    )

    search_fields = (
        '$name',
    )

    ordering_fields = (
        'name',
        'uploaded_on'
    )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(uploaded_by=user)


class APIRoot(generics.GenericAPIView):
    name = 'API Root'

    def get(self, request, *args, **kwargs):
        return Response({
            'obtain-auth-token': reverse('obtain-token', request=request),
            'users': reverse(CreateUserView.name, request=request),
            'posts': reverse(PostCreateList.name, request=request),
            'authors': reverse(AuthorList.name, request=request),
            'categories': reverse('category-list', request=request),
            'uploads': reverse(UploadImageView.name, request=request)
        })
