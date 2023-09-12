from django.db import models


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=64,)
    slug = models.SlugField('Слаг жанра', max_length=64,)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField('Название категории', max_length=64,)
    slug = models.SlugField('Слаг категории', max_length=64,)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=128)
    year = models.IntegerField('Год создания')
    rating = models.IntegerField('Рейтинг произведения', blank=True, null=True)
    # Поле rating временно реализовано с помощью IntegerField
    description = models.TextField(
        'Описание произведения', blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'
