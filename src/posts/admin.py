from django import forms
from django.contrib import admin
from .models import Post

from .models import Author, Category, Post
from django.conf.locale.en import formats as en_formats

en_formats.DATETIME_FORMAT = "d/m/y P"


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name', 'slug', 'is_main', 'get_posts_count')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'overview',
                    'author', 'slug', 'tag_list', 'is_published', 'modification_date', 'published_date')
    list_display_links = ('id', 'overview',)
    list_editable = ('is_published', )
    search_fields = ('title',)
    list_filter = ('is_published', 'tags', 'author',)
    ordering = ('id',)
    readonly_fields = ('published_date', )

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'overview', 'featured_image', 'content', 'tags', 'is_published', 'published_date')
        }),
        ('SEO Settings', {
            'fields': ('seo_title', 'seo_description')
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'display_name', 'bio')
    ordering = ('id',)
    list_display_links = ('user',)


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
