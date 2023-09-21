from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import filters, mixins, status
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpRequest
from django.db.utils import IntegrityError
from django.dispatch import Signal

from reviews.models import (
    Title,
    Review,
    Category,
    Comment,
    Genre,
)
from api.services import (
    get_all_objects,
    query_with_filter,
)
from api.serializers import (
    TitleGETSerilizer,
    TitlePOSTSerilizer,
    ReviewSerializer,
    CategorySerializer,
    UserSerializer,
    CommentSerializer,
    GenreSerializer,
    UserMeSerializer,
    AuthSerializer,
    SignUpSerializer,
)
from api.permissions import (
    IsAdminOrReadOnly,
    IsAdmin,
    AuthorAdminModeratorOrReadOnly,
)
from api.mixins import NoPutViewSetMixin
from api.filters import TitleFilter
from users.services import (
    get_tokens_for_user,
    generate_confirmation_code,
)


User = get_user_model()
code_generated = Signal()


class Auth(CreateAPIView):
    serializer_class = AuthSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer: AuthSerializer = self.serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
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


class Signup(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer: SignUpSerializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code: str = generate_confirmation_code()

        try:
            user, is_new = User.objects.get_or_create(
                **serializer.validated_data)
        except IntegrityError as err:
            error_field = err.args[0].split('.')[-1]
            raise ValidationError(
                {error_field: f'Provided {error_field} is already taken'})
        user.confirmation_code = confirmation_code
        user.save()

        code_generated.send(
            sender=Signup,
            confirmation_code=confirmation_code,
            user_email=user.email
        )
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )


class UsersViewSet(NoPutViewSetMixin, ModelViewSet):
    queryset = get_all_objects(User)
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    ordering = ('username',)

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])


class MeViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    queryset = get_all_objects(User)
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(User, username=self.request.user.username)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class TitleViewSet(NoPutViewSetMixin, ModelViewSet):
    queryset = get_all_objects(Title)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering = ('name',)

    def get_serializer_class(self) -> ModelSerializer:
        if self.request.method == 'GET':
            return TitleGETSerilizer
        return TitlePOSTSerilizer


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = get_all_objects(Category)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('name',)

    def get_object(self) -> Category:
        return get_object_or_404(Category, slug=self.kwargs.get('slug'))


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = get_all_objects(Genre)
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('name',)

    def get_object(self) -> Genre:
        return get_object_or_404(Genre, slug=self.kwargs.get('slug'))


class ReviewViewSet(NoPutViewSetMixin, ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('title',)

    def get_queryset(self):
        return query_with_filter(
            Review, {'title': self.kwargs.get('title_id')}
        )

    def perform_create(self, serializer):
        title = query_with_filter(
            Title, {'pk': self.kwargs.get('title_id')}, single=True
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(NoPutViewSetMixin, ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('-pub_date',)

    def get_queryset(self):
        return query_with_filter(
            Comment,
            {
                'review': self.kwargs.get('review_id'),
                'review__title': self.kwargs.get('title_id'),
            },
        )

    def perform_create(self, serializer):
        review = query_with_filter(
            Review,
            {
                'pk': self.kwargs.get('review_id'),
                'title': self.kwargs.get('title_id'),
            },
            single=True,
        )
        serializer.save(author=self.request.user, review=review)
