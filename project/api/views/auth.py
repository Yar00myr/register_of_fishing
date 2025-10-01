import logging

from django.contrib.auth import login
from rest_framework import generics, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from ..serializers import LoginSerializer


logger = logging.getLogger("api")


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as e:
            logger.warning(
                f"Failed login attempt: {request.data.get('email', 'N/A')} - {e}"
            )
            return Response({"errors": e.detail}, status=400)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        login(request, user)

        logger.info(f"User {user.username} logged in. Token created: {created}")
        return Response({"token": token.key})


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        username = request.user.username
        if hasattr(request.user, "auth_token"):
            request.user.auth_token.delete()
            logger.info(f"User {username} logged out and token deleted.")
        else:
            logger.warning(f"User {username} tried to logout but had no token.")
        return Response({"detail": "Logged out successfully"})
