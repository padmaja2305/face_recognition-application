'''
URL patterns
- /admin/ -> Admin pages
- /reboot -> Restart the server
- /monitor -> Monitor page for admin
- /image_recognition -> Image recognition API
- / -> Including URLs from api/urls.py
- STATIC_URL -> Static files serving
'''

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import ImageRecognition,  ImageReconMonitor, Reboot
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('image_recognition', ImageRecognition.as_view()),
    path('monitor', ImageReconMonitor.as_view()),
    path('reboot', Reboot.as_view()),
    path('', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
