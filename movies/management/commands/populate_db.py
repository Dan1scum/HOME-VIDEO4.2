from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from movies.models import Category, Genre, Movie, UserProfile


class Command(BaseCommand):
    help = 'Populate database with sample movie data'
    
    def handle(self, *args, **options):
        # Create categories
        categories = [
            Category.objects.get_or_create(name='Drama')[0],
            Category.objects.get_or_create(name='Action')[0],
            Category.objects.get_or_create(name='Comedy')[0],
            Category.objects.get_or_create(name='Horror')[0],
            Category.objects.get_or_create(name='Sci-Fi')[0],
        ]
        
        # Create genres
        genres = [
            Genre.objects.get_or_create(name='Adventure')[0],
            Genre.objects.get_or_create(name='Thriller')[0],
            Genre.objects.get_or_create(name='Romance')[0],
            Genre.objects.get_or_create(name='Mystery')[0],
        ]
        
        # Create sample user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            user.set_password('admin')
            user.save()
            UserProfile.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        
        # Create sample movies
        sample_movies = [
            {
                'title': 'Sample Movie 1',
                'description': 'This is a sample movie description',
                'category': categories[0],
                'author': user,
                'rating': 8.5
            },
            {
                'title': 'Sample Movie 2',
                'description': 'Another sample movie with an action-packed plot',
                'category': categories[1],
                'author': user,
                'rating': 7.2
            },
        ]
        
        for movie_data in sample_movies:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults=movie_data
            )
            if created:
                movie.genres.add(genres[0], genres[1])
                self.stdout.write(self.style.SUCCESS(f"Movie '{movie.title}' created"))
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
