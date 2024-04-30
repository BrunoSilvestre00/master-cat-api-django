from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView

from config.static import STATIC_ROOT, STATIC_URL, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    # path('admin/login/', LoginView.as_view(template_name='login-form.html'), name='login'),
    path('', include('core.urls')),
    path('admin/', admin.site.urls, name='admin'),
] + static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)

APP_NAME = "CAT API"
admin.site.site_header = f"{APP_NAME} Admin"
admin.site.site_title = f"{APP_NAME} Admin"
