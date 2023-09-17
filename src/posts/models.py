import uuid as uuid_lib

import readtime
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils import timezone
from taggit_selectize.managers import TaggableManager
from tinymce import HTMLField

from uploads.models import ImageUpload

# Create your models here.
User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=200, blank=True, null=True,
                                    help_text='Author\'s name as it will appear to their audience')
    short_description = models.CharField(
        max_length=50, help_text='Short info that might be used to describe author\'s job position or speciality.')
    bio = models.TextField(
        help_text='Longer info where they can describe author\'s hobbies, ideas and experience.')
    uuid = models.UUIDField(
        db_index=True, default=uuid_lib.uuid4, editable=False, help_text='A unique uuid auto generated used to identify each author.')

    class Meta:
        ordering = ('display_name', )

    @receiver(post_save, sender=User)
    def create_user_author(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_author(sender, instance, **kwargs):
        instance.author.save()

    def get_absolute_url(self):
        return reverse('blog_ui:author', kwargs={
            'author': self.user.username
        })

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=20, help_text='Name of the category.')
    slug = models.SlugField(
        unique=True, help_text='A unique \"slug\" consisting of letters, numbers, underscores or hyphens')
    is_main = models.BooleanField(
        verbose_name="Is Main Menu Item", default=False, help_text='Whether the category should be displayed in the main menu')

    def get_posts_count(self):
        return self.posts.count()
    get_posts_count.short_description = 'No. of Entries'

    def get_absolute_url(self):
        return reverse('blog_ui:category', kwargs={
            'category': self.slug
        })

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(
        max_length=100, help_text='Title of the blog post.')
    modification_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(unique=True, max_length=255,
                            help_text='A unique \"slug\" consisting of letters, numbers, underscores or hyphens')
    featured_image = models.ForeignKey(
        ImageUpload, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    overview = models.CharField(
        max_length=200, help_text='A short description about the blog post.')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="posts", blank=True, null=True, help_text='The category the blog post should be displayed under')
    tags = TaggableManager(
        help_text='An array of strings that represent tags for the post. ')
    content = HTMLField(help_text='Content of the post, including the markup.')
    is_published = models.BooleanField(
        default=False, help_text='Whether the post is visible on the blog or not')

    seo_title = models.CharField(max_length=60, help_text='The SEO title for the post. Site owners can create a different title for the browser title bar.', verbose_name='SEO Title')
    seo_description = models.CharField(max_length=160, help_text='The SEO page description for the post.', verbose_name='SEO Description')

    class Meta:
        ordering = ['published_date']

    def get_absolute_url(self):
        return reverse('blog_ui:post-detail', kwargs={
            'slug': self.slug
        })

    def get_read_time(self):
        return readtime.of_html(self.content)

    def save(self, *args, **kwargs):
        if self.is_published == True:
            self.published_date = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
