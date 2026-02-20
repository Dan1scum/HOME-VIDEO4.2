from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		verbose_name_plural = 'Categories'
		ordering = ['name']

	def __str__(self):
		return self.name
	
	def get_movie_count(self):
		return self.movies.count()


class Genre(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name
	
	def get_movie_count(self):
		return self.movies.count()


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	phone = models.CharField(max_length=20, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'User Profile'
		verbose_name_plural = 'User Profiles'
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.user.username} Profile'
	
	def get_absolute_url(self):
		return reverse('movies:user_profile', kwargs={'username': self.user.username})


class Movie(models.Model):
	title = models.CharField(max_length=200, db_index=True)
	description = models.TextField(blank=True)
	release_date = models.DateField(null=True, blank=True)
	poster = models.ImageField(upload_to='posters/', null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies')
	genres = models.ManyToManyField(Genre, blank=True, related_name='movies')
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='movies')
	rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [
			models.Index(fields=['title', '-created_at']),
			models.Index(fields=['-rating']),
		]

	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('movies:detail', kwargs={'pk': self.pk})
	
	def get_rating_display(self):
		return f"{self.rating}/10"
