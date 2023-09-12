from django.contrib import admin

from api.models import Title, Category, Genre


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    fields = ('name', 'year', 'rating', 'description', 'category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'slug',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ('name', 'slug',)
