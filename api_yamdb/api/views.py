from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.serializers import ModelSerializer

from api.models import Title
from api.services import get_all_objects
from api.serializers import TitleGETSerilizer, TitlePOSTSerilizer
from api.permissions import IsAdminOrReadOnly


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
