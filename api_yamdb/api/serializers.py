from rest_framework import serializers
from django.contrib.auth import get_user_model

from reviews.models import (
    Title,
    Genre,
    Category,
    Review
)
from api.services import get_all_objects, get_current_year


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


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
        year = get_current_year()
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
