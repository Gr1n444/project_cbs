from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True, unique=True)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='profile_images', default='profile_images/default.jpg')
    level = models.CharField(max_length=10, default='Beginner')
    points = models.IntegerField(default=0)
    event_points = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username