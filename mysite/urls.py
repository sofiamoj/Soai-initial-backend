"""
URL configuration for mysite project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('course/', include('course.urls', namespace='course')),
    path('services/', include('services.urls', namespace='services')),
    path('chat/', include('ai_assistant.urls', namespace='ai_assistant')),
]

# ✅ Fix: این خط کم بود - بدون این، Django فایل‌های media رو نشون نمیده
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)