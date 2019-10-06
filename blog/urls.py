from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from rest_framework import permissions, routers
from rest_framework.documentation import include_docs_urls

from .sitemaps import AuthorSitemap, CategorySitemap, PostSitemap
from api import urls

sitemaps = {
    'posts': PostSitemap,
    'authors': AuthorSitemap,
    'categories': CategorySitemap
}

API_TITLE = 'Coding Vortex Blog API'
API_DESCRIPTION = 'API to access data from our blog.'

urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('taggit/', include('taggit_selectize.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('contact/', include('contacts.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('posts.urls', namespace='posts')),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('api/v1/', include('api.urls')),
    path('api/docs/', include_docs_urls(title=API_TITLE,
                                        description=API_DESCRIPTION, patterns=urls.urlpatterns)),
]

admin.site.site_header = 'Coding Vortex Blog Admin'
admin.site.site_title = 'Coding Vortex Blog Admin'
