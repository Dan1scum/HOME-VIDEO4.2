from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	phone = models.CharField(max_length=20, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	try:
		instance.profile.save()
	except UserProfile.DoesNotExist:
		pass  # Profile will be created on access if needed


class Movie(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	release_date = models.DateField(null=True, blank=True)
	poster = models.ImageField(upload_to='posters/', null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies')
	genres = models.ManyToManyField(Genre, blank=True, related_name='movies')
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='movies')
	rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.title
