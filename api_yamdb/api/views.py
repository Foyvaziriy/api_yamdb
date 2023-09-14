import logging

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.serializers import ModelSerializer

from reviews.models import (
    Title,
    Review
)
from api.services import (
    get_all_objects,
    query_with_filter,
)
from api.serializers import (
    TitleGETSerilizer,
    TitlePOSTSerilizer,
    ReviewSerializer
)
from api.permissions import IsAdminOrReadOnly

log = logging.getLogger(__name__)


class TitleViewSet(ModelViewSet):
    queryset = get_all_objects(Title)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self) -> ModelSerializer:
        if self.request.method == 'GET':
            return TitleGETSerilizer
        return TitlePOSTSerilizer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
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
