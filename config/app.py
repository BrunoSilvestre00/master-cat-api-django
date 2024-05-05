# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_ckeditor_5',
    'django_light',
    'rest_framework',
    'rest_framework_swagger',
    'drf_yasg',
]

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'user.apps.UserConfig',
    'learning.apps.LearningConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
