from rest_framework import serializers
from django.contrib.auth import get_user_model
from reviews.models import (
    Title,
    Genre,
    Category,
    Review,
    Comment
)
from api.services import (
    get_all_objects,
    get_current_year,
    query_with_filter
)


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


class ReviewCommentSerializerAbstract(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    pub_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ', read_only=True)


class ReviewSerializer(ReviewCommentSerializerAbstract):
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = self.context['view'].kwargs['title_id']
            if query_with_filter(
                Review,
                {'title': title,
                 'author': self.context['request'].user
                 }).exists():
                raise serializers.ValidationError('Один пользователь может добавить '
                                                  'только один отзыв в рамках произведения')

        return data


class CommentSerializer(ReviewCommentSerializerAbstract):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
