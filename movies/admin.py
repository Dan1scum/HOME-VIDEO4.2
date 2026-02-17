from django.contrib import admin
from .models import Category, Genre, Movie, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'category', 'rating', 'release_date', 'created_at')
	list_filter = ('category', 'genres', 'created_at', 'author')
	search_fields = ('title', 'description', 'author__username')
	readonly_fields = ('created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'created_at', 'updated_at')
	search_fields = ('user__username', 'user__email')
	readonly_fields = ('user', 'created_at', 'updated_at')

