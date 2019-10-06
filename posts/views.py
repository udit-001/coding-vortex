from pprint import pprint
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import generics, viewsets
from taggit.models import Tag

from .models import Author, Category, Post


def post_list(request):
    post_list = Post.objects.select_related('author','category').filter(
        is_published=True).order_by('-published_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts
    }

    return render(request, 'posts/index.html', context)


def post_categories(request, category):
    category_item = get_object_or_404(Category, slug=category)
    post_list = get_list_or_404(
        category_item.posts.select_related('author', 'category').filter(is_published=True))
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'title': category_item.name,
        'subtitle': f"{post_list.__len__()} posts in {category_item.name}",
        'posts': posts
    }
    return render(request, 'posts/results.html', context)


def post_tags(request, tag):
    tag_item = Tag.objects.get(slug=tag)
    post_list = get_list_or_404(Post.objects.select_related('author', 'category'), tags__slug__in=[tag, ])
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'title': tag_item.name,
        'subtitle': f"{paginator.count} posts in {tag_item.name}",
        'posts': posts
    }
    return render(request, 'posts/results.html', context)


def post_details(request, slug):
    post = get_object_or_404(Post.objects.select_related('author', 'featured_image', 'category'), slug=slug, is_published=True)
    context = {
        'post': post,
        'related_posts': Post.objects.filter(is_published=True, tags__name__in=list(post.tags.values_list('name', flat=True))).exclude(id=post.id).distinct()
    }
    return render(request, 'posts/post.html', context)


def post_search(request):
    request_parameter = 'q'
    query = request.GET.get(request_parameter)
    post_list = Post.objects.select_related('author', 'category').filter(
        Q(title__icontains=query) | Q(overview__icontains=query) | Q(content__icontains=query), is_published=True).order_by('published_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'title': 'Search',
        'subtitle': f"{posts.paginator.count} Results found for \"{query}\"",
        'request_parameter': request_parameter,
        'posts': posts
    }

    return render(request, 'posts/results.html', context)


def about_author(request, author):
    author_item = get_object_or_404(Author, user__username=author)
    context = {
        'author': author_item
    }
    return render(request, 'posts/about.html', context)
