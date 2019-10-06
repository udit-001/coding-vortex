from django.urls import path
from . import views

app_name = 'blog_ui'

urlpatterns = [
    path('', views.post_list, name='home'),
    path('tag/<slug:tag>/', views.post_tags, name="tag"),
    path('category/<slug:category>/', views.post_categories, name="category"),
    path('search/', views.post_search, name='post-search'),
    path('about/<author>/', views.about_author, name='author'),
    path('<slug:slug>/', views.post_details, name="post-detail"),
]
