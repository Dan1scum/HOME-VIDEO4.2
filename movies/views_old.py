from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, Count, F

from .models import Movie, Category, Genre, UserProfile
from .forms import MovieForm, RegisterForm, UserProfileForm, MovieEditForm
from .utils import filter_movies, get_movie_context


class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12
    
    def get_queryset(self):
        qs = Movie.objects.all().select_related('category', 'author').prefetch_related('genres')
        
        search = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category')
        genres = self.request.GET.getlist('genre')
        sort = self.request.GET.get('sort', '-created_at')
        
        if search:
            tokens = [t for t in search.split() if t]
            q_obj = Q()
            for token in tokens:
                q_obj &= (Q(title__icontains=token) | Q(description__icontains=token))
            qs = qs.filter(q_obj)
        
        if category:
            try:
                qs = qs.filter(category__id=int(category))
            except (ValueError, TypeError):
                pass
        
        if genres:
            try:
                genre_ids = [int(g) for g in genres]
                qs = qs.filter(genres__id__in=genre_ids).distinct()
            except (ValueError, TypeError):
                pass
        
        valid_sorts = ['-created_at', 'created_at', 'title', '-title', '-rating', 'rating']
        if sort in valid_sorts:
            qs = qs.order_by(sort)
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['genres'] = Genre.objects.all()
        context['q'] = self.request.GET.get('q', '')
        context['category'] = self.request.GET.get('category', '')
        context['sort'] = self.request.GET.get('sort', '-created_at')
        
        genres_selected = self.request.GET.getlist('genre')
        try:
            context['selected_genres'] = [int(g) for g in genres_selected]
        except (ValueError, TypeError):
            context['selected_genres'] = []
        
        return context


class AjaxFilterView(View):
    def get(self, request):
        qs = Movie.objects.all().select_related('category', 'author').prefetch_related('genres')
        
        search = request.GET.get('q', '').strip()
        category = request.GET.get('category')
        genres = request.GET.getlist('genre')
        
        if search:
            tokens = [t for t in search.split() if t]
            q_obj = Q()
            for token in tokens:
                q_obj &= (Q(title__icontains=token) | Q(description__icontains=token))
            qs = qs.filter(q_obj)
        
        if category:
            try:
                qs = qs.filter(category__id=int(category))
            except (ValueError, TypeError):
                pass
        
        if genres:
            try:
                genre_ids = [int(g) for g in genres]
                qs = qs.filter(genres__id__in=genre_ids).distinct()
            except (ValueError, TypeError):
                pass
        
        return render(request, 'movies/_movie_cards.html', {'movies': qs})
        if genres_selected:
            qs = qs.filter(genres__id__in=genres_selected).distinct()
        
        return render(request, 'movies/_movie_cards.html', {'movies': qs})


class MovieDetailView(DetailView):
    """Детальный просмотр фильма"""
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = (
            self.object.author == self.request.user 
            if self.request.user.is_authenticated else False
        )
        return context


class MovieCreateView(LoginRequiredMixin, CreateView):
    """Создание нового фильма"""
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_create.html'
    
    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.author = self.request.user
        movie.save()
        form.save_m2m()
        messages.success(self.request, 'Movie created successfully')
        return redirect('movies:detail', pk=movie.pk)


class MovieEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование фильма"""
    model = Movie
    form_class = MovieEditForm
    template_name = 'movies/movie_edit.html'
    context_object_name = 'movie'
    
    def test_func(self):
        movie = self.get_object()
        return movie.author == self.request.user or self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to edit this movie')
        return redirect('movies:detail', pk=self.get_object().pk)
    
    def get_success_url(self):
        messages.success(self.request, 'Movie updated successfully')
        return reverse_lazy('movies:detail', kwargs={'pk': self.object.pk})


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление фильма"""
    model = Movie
    template_name = 'movies/movie_delete.html'
    success_url = reverse_lazy('movies:list')
    context_object_name = 'movie'
    
    def test_func(self):
        movie = self.get_object()
        return movie.author == self.request.user or self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to delete this movie')
        return redirect('movies:detail', pk=self.get_object().pk)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Movie deleted successfully')
        return super().delete(request, *args, **kwargs)


class RegisterView(CreateView):
    """Регистрация пользователя"""
    form_class = RegisterForm
    template_name = 'movies/register.html'
    success_url = reverse_lazy('movies:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Registration successful. You can now log in.')
        return super().form_valid(form)


class ProfileView(DetailView):
    """Просмотр профиля пользователя"""
    model = User
    template_name = 'movies/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        if username:
            return get_object_or_404(User, username=username)
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Please log in to view your profile')
            return redirect('movies:login')
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['profile_user']
        
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        context['profile'] = profile
        context['user_movies'] = user.movies.all()
        context['is_owner'] = user == self.request.user if self.request.user.is_authenticated else False
        
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'movies/profile_edit.html'
    context_object_name = 'profile'
    
    def get_object(self, queryset=None):
        try:
            profile = self.request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=self.request.user)
        return profile
    
    def get_success_url(self):
        messages.success(self.request, 'Profile updated successfully')
        return reverse_lazy('movies:profile', kwargs={'username': self.request.user.username})


# Функция для обратной совместимости (если используется в других местах)
def movie_list(request):
    return MovieListView.as_view()(request)

def ajax_filter(request):
    return AjaxFilterView.as_view()(request)

def movie_detail(request, pk):
    return MovieDetailView.as_view()(request, pk=pk)

def movie_create(request):
    return MovieCreateView.as_view()(request)

def movie_edit(request, pk):
    return MovieEditView.as_view()(request, pk=pk)

def movie_delete(request, pk):
    return MovieDeleteView.as_view()(request, pk=pk)

def register_view(request):
    return RegisterView.as_view()(request)

def profile_view(request, username=None):
    return ProfileView.as_view()(request, username=username)

def profile_edit(request):
    return ProfileEditView.as_view()(request)

