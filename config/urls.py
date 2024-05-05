from django.conf.urls import include
from django.urls import path, re_path
from django.views.static import serve
from django.contrib import admin

from config.static import STATIC_ROOT, MEDIA_ROOT


APP_URLS = [
    path('', include('core.urls')),
]

DJANGO_URLS = [
    path('admin/', admin.site.urls, name='admin'),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
]

STATIC_URLS = [
    re_path(r'^media/(?P<path>.*)$', serve, { 'document_root': MEDIA_ROOT }),
    re_path(r'^static/(?P<path>.*)$', serve, { 'document_root': STATIC_ROOT }),
]

urlpatterns = APP_URLS + DJANGO_URLS + STATIC_URLS

APP_NAME = "CAT API"
admin.site.site_header = f"{APP_NAME} Admin"
admin.site.site_title = f"{APP_NAME} Admin"
