from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    full_text = models.TextField()
    category = models.CharField(max_length=30)
    pubdate = models.DateTimeField()
    slug = models.CharField(max_length=255, unique=True)
    title_image = models.ImageField(upload_to='article_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_page', kwargs={'slug': self.slug})

    def get_category_url(self):
        return reverse('category_page', kwargs={'category': self.category})
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'