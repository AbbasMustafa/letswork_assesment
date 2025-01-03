from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from event_management.users.models import User

from .serializers import SignupSerializer
from .serializers import UserSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("-pk")
    lookup_field = "username"

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {
                    "data": None,
                    "message": "You do not have permission to perform this action.",
                    "status": False,
                    "status_code": status.HTTP_403_FORBIDDEN,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "data": response.data,
                "message": "User list retrieved successfully",
                "status": True,
                "status_code": status.HTTP_200_OK,
            },
        )

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(
            {
                "data": serializer.data,
                "message": "User details retrieved successfully",
                "status": True,
                "status_code": status.HTTP_200_OK,
            },
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user, context={"request": request}).data
            return Response(
                {
                    "data": user_data,
                    "message": "User created successfully",
                    "status": True,
                    "status_code": status.HTTP_201_CREATED,
                },
            )
        return Response(
            {
                "data": serializer.errors,
                "message": "Signup failed",
                "status": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
            },
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "data": {"token": token.key},
                    "message": "Signin successful",
                    "status": True,
                    "status_code": status.HTTP_200_OK,
                },
            )
        return Response(
            {
                "data": None,
                "message": "Invalid username or password",
                "status": False,
                "status_code": status.HTTP_401_UNAUTHORIZED,
            },
        )
