from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import filters
from rest_framework.serializers import ModelSerializer
from rest_framework import mixins
from django.shortcuts import get_object_or_404

from reviews.models import Title, Category
from api.services import get_all_objects
from api.serializers import (
    TitleGETSerilizer, TitlePOSTSerilizer, CategorySerializer)
from api.permissions import IsAdminOrReadOnly


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

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['slug'])
