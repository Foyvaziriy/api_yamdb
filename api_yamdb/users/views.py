from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpRequest
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from users.serializers import AuthSerializer, SignUpSerializer
from users.services import get_tokens_for_user


User = get_user_model()


class Auth(CreateAPIView):
    serializer_class = AuthSerializer

    def post(self, request: HttpRequest) -> Response:
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                user = get_object_or_404(
                    User,
                    username=data.get('username'),
                    confirmation_code=data.get('confirmation_code'),
                )
                tokens = get_tokens_for_user(user)
                return Response(
                    tokens,
                    status=status.HTTP_200_OK,
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Http404:
            return Response(
                {'detail': 'User with provided data not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )


class Signup(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            confirmation_code = '115143'  # вот тут генерацию кода
            user = User.objects.filter(**request.data)
            if user:
                user = user[0]
                user.confirmation_code = confirmation_code
                user.save()
                # send_code(confirmation_code, user.email)
                return Response(
                    serializer.validated_data,
                    status=status.HTTP_200_OK,
                )
            new_user = User.objects.create(
                **serializer.validated_data,
                confirmation_code=confirmation_code
            )
            # send_code(confirmation_code, user.email)
            return Response(
                {
                    'username': new_user.username,
                    'email': new_user.email
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
