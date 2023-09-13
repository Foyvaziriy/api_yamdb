from rest_framework import serializers
from django.utils import timezone


from reviews.models import Title, Genre, Category
from api.services import get_all_objects

from api_yamdb.reviews.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


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
        queryset=get_all_objects(Genre),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=get_all_objects(Category))

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
    genre = GenreSerializer(read_only=False, many=True)
    category = CategorySerializer(read_only=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'category', 'genre')
