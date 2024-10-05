from django.urls import path
from app_blog.views import *



urlpatterns = [
    path('articles', articles, name='articles'),
    path('article/<slug:slug>/', article_page, name='article_page'),
    path('article/category/<slug:category>/', category_page, name='category_page'),
]

