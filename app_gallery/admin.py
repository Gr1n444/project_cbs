from django.contrib import admin
from app_gallery.models import Image


admin.site.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass