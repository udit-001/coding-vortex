from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from taggit.models import Tag
from taggit_serializer.serializers import (TaggitSerializer,
                                           TagListSerializerField)

from posts import models
from uploads.models import ImageUpload


class PostSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = models.Post
        lookup_field = 'slug'
        read_only_fields = ['author', ]
        fields = (
            'title',
            'author',
            'overview',
            'content',
            'featured_image',
            'published_date',
            'category',
            'tags',
            'slug',
            'url',
            'is_published'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'published_date': {
                'read_only': True
            }
        }

    author = serializers.ReadOnlyField(source='author.display_name')

    category = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(), slug_field='name')
    featured_image = serializers.SlugRelatedField(
        queryset=ImageUpload.objects.all(), slug_field='name')


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    posts = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='post-detail', lookup_field='slug')

    class Meta:
        model = models.Author
        lookup_field = 'uuid'
        fields = (
            'uuid',
            'display_name',
            'user',
            'short_description',
            'bio',
            'url',
            'posts'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='post-detail', lookup_field='slug')

    class Meta:
        model = models.Category
        lookup_field = 'slug'
        fields = (
            'slug',
            'name',
            'url',
            'posts'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CreateUserSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail',
        lookup_field='uuid',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
            'author'
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        if validated_data.get('email', None):
            user = User(email=validated_data['email'],
                        username=validated_data['username']
                        )
        else:
            user = User(username=validated_data['username']
                        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ImageUploadSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(
        source='uploaded_by.author.display_name')

    class Meta:
        model = ImageUpload
        fields = (
            'name',
            'image',
            'uploaded_on',
            'uploaded_by'
        )
        read_only_fields = ['uploaded_by', ]
