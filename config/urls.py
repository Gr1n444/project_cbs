from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('administrator/', admin.site.urls),
    path('', include('app_blog.urls')),
    path('', include('app_task.urls')),
    path('', include('app_test.urls')),
    path('', include('app_users.urls')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

