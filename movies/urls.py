from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='list'),
    path('movie/<int:pk>/', views.movie_detail, name='detail'),
    path('create/', views.movie_create, name='create'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='movies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='movies:list'), name='logout'),
]
