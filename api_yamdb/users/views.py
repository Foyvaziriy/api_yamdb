from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpRequest
from rest_framework import mixins, viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.services import get_all_objects
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


class Signup(mixins.CreateModelMixin,
             viewsets.GenericViewSet):
    queryset = get_all_objects(User)
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        confirmation_code = '1235'  # вот тут генерацию кода

        # Вот тут надо настроить отсылку письма с кодом
        serializer.save(confirmation_code=confirmation_code)
