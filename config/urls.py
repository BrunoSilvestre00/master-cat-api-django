from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

from config.static import STATIC_ROOT, STATIC_URL

urlpatterns = [
    # path('admin/login/', LoginView.as_view(template_name='login-form.html'), name='login'),
    path('admin/', admin.site.urls, name='admin'),
] + static(STATIC_URL, document_root=STATIC_ROOT)

APP_NAME = "CAT API"
admin.site.site_header = f"{APP_NAME} Admin"
admin.site.site_title = f"{APP_NAME} Admin"
