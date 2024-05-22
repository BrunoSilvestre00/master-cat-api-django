from decouple import config as env

SECRET_KEY = env('SECRET_KEY')

HOSTS = [
    '127.0.0.1:8000', 'localhost:8000', 'cbt2.icmc.usp.br:8000',
]

ALLOWED_HOSTS = [
    '127.0.0.1', 'localhost', 'cbt2.icmc.usp.br',
]

CSRF_TRUSTED_ORIGINS = [f'http://{host}' for host in HOSTS]

CORS_ORIGIN_WHITELIST = [f'http://{host}' for host in HOSTS]

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'
