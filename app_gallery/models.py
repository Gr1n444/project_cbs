from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/articles')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'