from django.contrib import admin
from app_blog.models import Article

admin.site.register(Article)

class ArticleAdmin(admin.ModelAdmin):
    pass
