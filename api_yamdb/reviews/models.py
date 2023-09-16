from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from api.services import get_current_year


User = get_user_model()


class Genre(models.Model):
    name = models.CharField('genre name', max_length=256,)
    slug = models.SlugField('genre slug', max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField('category name', max_length=256,)
    slug = models.SlugField('category slug', max_length=50, unique=True,)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField('title name', max_length=128)
    year = models.IntegerField('release year')
    description = models.TextField(
        'title description', blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=get_current_year()),
                name='invalid year',
            ),
        ]

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Текст отзыва')
    score = models.IntegerField(
        'Оценка пользователя',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True)
