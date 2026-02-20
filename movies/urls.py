from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'movies'

urlpatterns = [
    # Movie URLs
    path('', views.MovieListView.as_view(), name='list'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='detail'),
    path('movie/<int:pk>/edit/', views.MovieEditView.as_view(), name='edit'),
    path('movie/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='delete'),
    path('create/', views.MovieCreateView.as_view(), name='create'),
    path('ajax/filter/', views.AjaxFilterView.as_view(), name='ajax_filter'),
    
    # User & Auth URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='movies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='movies:list'), name='logout'),
    
    # Profile URLs (профиль/edit/ ДОЛЖЕН быть ДО профиля/<username>/)
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='user_profile'),
]



