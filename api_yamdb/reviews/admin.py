from django.contrib import admin

from reviews.models import Title, Category, Genre, Review


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    fields = ('name', 'year', 'rating', 'description', 'category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'slug',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ('name', 'slug',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ('author', 'text', 'score', 'title')
