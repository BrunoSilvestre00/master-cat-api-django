import uuid
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from user.models import User, UserToken


class UserAuthViewset(viewsets.GenericViewSet):

    def get_serializer(self, *args, **kwargs):
        return None

    @action(methods=["POST"], detail=False, url_path="login", url_name="login")
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = UserToken.objects.get_or_create(
            user=user, defaults={"token": uuid.uuid4().__str__()}
        )
        data = {
            "token": token.token,
            "user_id": user.uuid,
        }
        return Response(data, status=status.HTTP_200_OK)
