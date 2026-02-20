from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Movie, Category, Genre, UserProfile


class MovieListViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Drama')
        cls.genre = Genre.objects.create(name='Action')
        
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        cls.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            category=cls.category,
            author=cls.user,
            rating=8.5
        )
        cls.movie.genres.add(cls.genre)
    
    def setUp(self):
        self.client = Client()
    
    def test_list_view_status_code(self):
        response = self.client.get(reverse('movies:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_list_view_uses_correct_template(self):
        response = self.client.get(reverse('movies:list'))
        self.assertTemplateUsed(response, 'movies/movie_list.html')
    
    def test_list_view_pagination(self):
        response = self.client.get(reverse('movies:list'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == False)
    
    def test_list_view_contains_movies(self):
        response = self.client.get(reverse('movies:list'))
        self.assertContains(response, 'Test Movie')


class MovieDetailViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Drama')
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.movie = Movie.objects.create(
            title='Test Movie',
            category=cls.category,
            author=cls.user
        )
    
    def setUp(self):
        self.client = Client()
    
    def test_detail_view_status_code(self):
        response = self.client.get(reverse('movies:detail', kwargs={'pk': self.movie.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('movies:detail', kwargs={'pk': self.movie.pk}))
        self.assertTemplateUsed(response, 'movies/movie_detail.html')


class MovieCreateViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Drama')
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def setUp(self):
        self.client = Client()
    
    def test_create_view_requires_login(self):
        response = self.client.get(reverse('movies:create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('movies:create'))
        self.assertEqual(response.status_code, 200)


class UserProfileTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_user_profile_created_on_user_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
