from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import filters
from rest_framework.serializers import ModelSerializer
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from reviews.models import (
    Title,
    Review,
    Category,
    Comment
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
    CommentSerializer
)
from api.permissions import (
    IsAdminOrReadOnly,
    IsAdmin,
    AuthorAdminModeratorOrReadOnly
)
from api.mixins import NoPutViewSetMixin

User = get_user_model()


class UsersViewSet(ModelViewSet):
    queryset = get_all_objects(User)
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)


class TitleViewSet(ModelViewSet):
    queryset = get_all_objects(Title)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self) -> ModelSerializer:
        if self.request.method == 'GET':
            return TitleGETSerilizer
        return TitlePOSTSerilizer


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = get_all_objects(Category)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_object(self) -> Category:
        return get_object_or_404(Category, slug=self.kwargs['slug'])


class ReviewViewSet(NoPutViewSetMixin, ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('title',)

    def get_queryset(self):
        return query_with_filter(
            Review,
            {'title': self.kwargs.get('title_id')}
        )

    def perform_create(self, serializer):
        title = query_with_filter(
            Title,
            {'pk': self.kwargs.get('title_id')},
            single=True
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(NoPutViewSetMixin, ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('-pub_date',)

    def get_queryset(self):
        return query_with_filter(
            Comment,
            {'review': self.kwargs.get('review_id'),
             'review__title': self.kwargs.get('title_id')
             }
        )

    def perform_create(self, serializer):
        review = query_with_filter(
            Review,
            {'pk': self.kwargs.get('review_id'),
             'title': self.kwargs.get('title_id')
             },
            single=True
        )
        serializer.save(
            author=self.request.user,
            review=review
        )
