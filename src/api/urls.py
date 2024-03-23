from django.urls import path
from rest_framework.documentation import include_docs_urls
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('',
         views.APIRoot.as_view(),
         name=views.APIRoot.name),
    path('obtain-token-auth/', obtain_auth_token, name='obtain-token'),
    path('users/', views.CreateUserView.as_view(),
         name=views.CreateUserView.name),
    path('posts/', views.PostCreateList.as_view(),
         name=views.PostCreateList.name),
    path('posts/<slug:slug>', views.PostDetail.as_view(),
         name=views.PostDetail.name),
    path('authors/', views.AuthorList.as_view(),
         name=views.AuthorList.name),
    path('authors/<uuid:uuid>', views.AuthorDetail.as_view(),
         name='author-detail'),
    path('categories/', views.CategoryListView.as_view(),
         name=views.CategoryListView.name),
    path('categories/<slug:slug>', views.CategoryDetailView.as_view(),
         name=views.CategoryDetailView.name),
    path('uploads/', views.UploadImageView.as_view(),
         name=views.UploadImageView.name)
]
