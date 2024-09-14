from django.utils.deprecation import MiddlewareMixin

from core.auth import TokenAuthentication


class AuthUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            user, _ = TokenAuthentication().authenticate(request)
            if user:
                request.user = user
        except:
            pass
