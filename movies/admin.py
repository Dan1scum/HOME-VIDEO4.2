from django.contrib import admin
from .models import Category, Genre, Movie, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'get_movie_count')
	search_fields = ('name',)
	ordering = ('name',)
	
	def get_movie_count(self, obj):
		return obj.get_movie_count()
	get_movie_count.short_description = 'Movies'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ('name', 'get_movie_count')
	search_fields = ('name',)
	ordering = ('name',)
	
	def get_movie_count(self, obj):
		return obj.get_movie_count()
	get_movie_count.short_description = 'Movies'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'category', 'rating', 'release_date', 'created_at', 'get_genres')
	list_filter = ('category', 'genres', 'created_at', 'author', 'rating')
	search_fields = ('title', 'description', 'author__username')
	readonly_fields = ('created_at', 'updated_at')
	list_per_page = 25
	
	fieldsets = (
		('Основная информация', {
			'fields': ('title', 'description', 'category', 'genres')
		}),
		('Метаданные', {
			'fields': ('author', 'release_date', 'poster', 'rating')
		}),
		('Даты', {
			'fields': ('created_at', 'updated_at'),
			'classes': ('collapse',)
		}),
	)
	
	def get_genres(self, obj):
		return ', '.join([g.name for g in obj.genres.all()])
	get_genres.short_description = 'Genres'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'get_bio_preview', 'created_at', 'updated_at')
	search_fields = ('user__username', 'user__email', 'bio')
	readonly_fields = ('user', 'created_at', 'updated_at')
	list_per_page = 25
	
	def get_bio_preview(self, obj):
		return obj.bio[:50] + '...' if len(obj.bio) > 50 else obj.bio
	get_bio_preview.short_description = 'Bio'



