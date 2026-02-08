from django.contrib import admin
from .models import Category, Genre, Movie


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'release_date', 'created_at')
	list_filter = ('category', 'genres')
	search_fields = ('title', 'description')
