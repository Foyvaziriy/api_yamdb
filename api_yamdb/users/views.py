from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.db.models.query import QuerySet

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from users.serializers import AuthSerializer, SignUpSerializer
from users.services import (
    get_tokens_for_user,
    generate_confirmation_code,
    send_code,
)
from api.services import get_all_objects, query_with_filter, create_object


User = get_user_model()


class Auth(CreateAPIView):
    serializer_class = AuthSerializer

    def post(self, request: HttpRequest) -> Response:
            serializer: AuthSerializer = self.serializer_class(
                data=request.data
            )
            if serializer.is_valid():
                data = serializer.validated_data
                user = get_object_or_404(
                    User,
                    username=data.get('username'),
                )
                if user.confirmation_code != data.get('confirmation_code'):
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response(
                    get_tokens_for_user(user),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )


class Signup(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer: SignUpSerializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            confirmation_code: str = generate_confirmation_code()

            names_emails: dict[str, str] = dict()
            for user in get_all_objects(User):
                names_emails[user.username] = user.email

            username: str = serializer.validated_data.get('username')
            email: str = serializer.validated_data.get('email')
            msg: str = "'{}' is already taken."

            user: QuerySet = query_with_filter(
                User, filter_dict=serializer.validated_data
            )

            if user:
                user = user[0]
                user.confirmation_code = confirmation_code
                user.save()
                send_code(
                    user_email=user.email,
                    confirmation_code=confirmation_code,
                )
                return Response(
                    serializer.validated_data,
                    status=status.HTTP_200_OK,
                )
            if username in names_emails:
                return Response(
                    {'detail': f'username {msg.format(username)}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if email in names_emails.values():
                return Response(
                    {'detail': f'email {msg.format(email)}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            new_user = create_object(
                User,
                **serializer.validated_data,
                confirmation_code=confirmation_code,
            )
            send_code(
                user_email=new_user.email,
                confirmation_code=confirmation_code,
            )
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
