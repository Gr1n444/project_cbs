from django.shortcuts import render
from .models import Article
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_page


global_context = {
    'author_name': _('Школа кибербезопасности'),
}

@cache_page(60*15)
def articles(request):
    articles = Article.objects.order_by('-pubdate')
    context = global_context | {'articles': articles}
    return render(request, 'articles.html', context)

@cache_page(60*15)
def article_page(request, slug):
    article = Article.objects.get(slug=slug)
    context = global_context | {'article': article}
    return render(request, 'article_page.html', context)

@cache_page(60*15)
def category_page(request, category):
    articles = Article.objects.filter(category=category)
    context = global_context | {'articles': articles, 'category': category}
    return render(request, 'category_page.html', context)