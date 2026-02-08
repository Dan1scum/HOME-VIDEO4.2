from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name


class Genre(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name


class Movie(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	release_date = models.DateField(null=True, blank=True)
	poster = models.ImageField(upload_to='posters/', null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies')
	genres = models.ManyToManyField(Genre, blank=True, related_name='movies')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title
