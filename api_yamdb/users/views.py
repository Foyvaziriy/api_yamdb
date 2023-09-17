from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpRequest
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from users.serializers import AuthSerializer, SignUpSerializer
from users.services import (
    get_tokens_for_user, generate_confirmation_code, send_code)


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
        serializer: SignUpSerializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            confirmation_code: str = generate_confirmation_code()

            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')

            user_by_username: QuerySet = User.objects.filter(username=username)
            user_by_email: QuerySet = User.objects.filter(email=email)

            if bool(user_by_username) and bool(user_by_email):
                user = get_object_or_404(User, **serializer.validated_data)
                user.confirmation_code = confirmation_code
                user.save()
                send_code(
                    user_email=user.email,
                    confirmation_code=confirmation_code
                )
                return Response(
                    serializer.validated_data,
                    status=status.HTTP_200_OK,
                )
            elif user_by_username:
                return Response(
                    {
                        'username': f'user with username {username} is already exists.'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif user_by_email:
                return Response(
                    {
                        'username': f'user with email {email} is already exists.'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            new_user = User.objects.create(
                **serializer.validated_data,
                confirmation_code=confirmation_code
            )
            send_code(
                user_email=new_user.email,
                confirmation_code=confirmation_code
            )
            return Response(
                {
                    'username': new_user.username,
                    'email': new_user.email
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
