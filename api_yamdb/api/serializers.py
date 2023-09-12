from rest_framework import serializers
from django.utils import timezone

from api.models import Title, Genre, Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class TitlePOSTSerilizer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'category', 'genre')

    def validate_year(self, value: int) -> int:
        year = timezone.now().year
        if value > year:
            raise serializers.ValidationError('Проверьте дату выхода')
        return value


class TitleGETSerilizer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'category', 'genre')
