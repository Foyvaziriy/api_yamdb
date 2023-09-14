from django.db import models

from api.services import get_current_year


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
    rating = models.IntegerField('title rating', blank=True, null=True)
    # Поле rating временно реализовано с помощью IntegerField
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
