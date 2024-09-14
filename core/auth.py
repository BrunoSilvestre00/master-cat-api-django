from typing import Optional

from user.models import User, UserToken


class TokenAuthentication(object):

    def get_user(self, token) -> Optional[User]:
        try:
            token = UserToken.objects.get(token=token)
            return token.user
        except UserToken.DoesNotExist:
            return None

    def authenticate(self, request) -> tuple:
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return None, None
        token = token.split(" ")[1]
        user = self.get_user(token)
        return user, None
