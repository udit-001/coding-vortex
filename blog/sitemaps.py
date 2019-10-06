from django.contrib.sitemaps import Sitemap
from django.db.models import Count

from posts.models import Author, Category, Post


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_date

class AuthorSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return  Author.objects.filter()

class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        all_categories = Category.objects.annotate(Count('posts'))

        not_empty_categories = all_categories.filter(posts__count__gt=0)

        return not_empty_categories
