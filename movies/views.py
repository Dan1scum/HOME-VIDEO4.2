from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Category, Genre, UserProfile
from .forms import MovieForm, RegisterForm, UserProfileForm, MovieEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.http import HttpResponseForbidden


def movie_list(request):
    qs = Movie.objects.all().order_by('-created_at')
    q = request.GET.get('q')
    cat = request.GET.get('category')
    genres_selected = request.GET.getlist('genre')
    sort_by = request.GET.get('sort', '-created_at')

    if q:
        q_clean = q.strip()
        # split query into tokens and filter by each token (case-insensitive)
        tokens = [t for t in q_clean.split() if t]
        if tokens:
            qs = qs.annotate(title_lower=Lower('title'))
            for t in tokens:
                qs = qs.filter(title_lower__contains=t.lower())
    if cat:
        qs = qs.filter(category__id=cat)
    if genres_selected:
        # filter by any of the selected genres (many-to-many)
        qs = qs.filter(genres__id__in=genres_selected).distinct()

    # Валидная сортировка
    valid_sorts = ['-created_at', 'created_at', 'title', '-title']
    if sort_by in valid_sorts:
        qs = qs.order_by(sort_by)

    # Пагинация (10 фильмов на странице)
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    # Все жанры для фильтрации
    all_genres = Genre.objects.all()
    # нормализуем выбранные жанры в список int для шаблона
    try:
        selected_genres = [int(x) for x in genres_selected]
    except Exception:
        selected_genres = []

    context = {
        'movies': movies,
        'q': q,
        'cat': cat,
        'sort_by': sort_by,
        'genres': all_genres,
        'selected_genres': selected_genres,
    }
    return render(request, 'movies/movie_list.html', context)


def ajax_filter(request):
    """Возвращает HTML-фрагмент с карточками фильтрованных фильмов (для AJAX)."""
    qs = Movie.objects.all().order_by('-created_at')
    q = request.GET.get('q')
    cat = request.GET.get('category')
    genres_selected = request.GET.getlist('genre')

    if q:
        q_clean = q.strip()
        tokens = [t for t in q_clean.split() if t]
        if tokens:
            qs = qs.annotate(title_lower=Lower('title'))
            for t in tokens:
                qs = qs.filter(title_lower__contains=t.lower())
    if cat:
        qs = qs.filter(category__id=cat)
    if genres_selected:
        qs = qs.filter(genres__id__in=genres_selected).distinct()

    return render(request, 'movies/_movie_cards.html', {'movies': qs})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    context = {
        'movie': movie,
        'is_author': movie.author == request.user if request.user.is_authenticated else False,
    }
    return render(request, 'movies/movie_detail.html', context)


@login_required
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.author = request.user
            movie.save()
            form.save_m2m()
            messages.success(request, 'Movie created successfully')
            return redirect('movies:detail', pk=movie.pk)
    else:
        form = MovieForm()
    return render(request, 'movies/movie_create.html', {'form': form})


@login_required
def movie_edit(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    # Проверяем, является ли пользователь автором
    if movie.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this movie')
        return redirect('movies:detail', pk=pk)
    
    if request.method == 'POST':
        form = MovieEditForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie updated successfully')
            return redirect('movies:detail', pk=movie.pk)
    else:
        form = MovieEditForm(instance=movie)
    
    context = {'form': form, 'movie': movie}
    return render(request, 'movies/movie_edit.html', context)


@login_required
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    # Проверяем, является ли пользователь автором
    if movie.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this movie')
        return redirect('movies:detail', pk=pk)
    
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully')
        return redirect('movies:list')
    
    context = {'movie': movie}
    return render(request, 'movies/movie_delete.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('movies:login')
    else:
        form = RegisterForm()
    return render(request, 'movies/register.html', {'form': form})


def profile_view(request, username=None):
    """View user profile"""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to view your profile')
            return redirect('movies:login')
        user = request.user
    
    # Проверяем наличие профиля
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    user_movies = user.movies.all() if hasattr(user, 'movies') else Movie.objects.filter(author=user)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'user_movies': user_movies,
        'is_owner': user == request.user if request.user.is_authenticated else False,
    }
    return render(request, 'movies/profile.html', context)


@login_required
def profile_edit(request):
    """Edit user profile"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('movies:profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'movies/profile_edit.html', context)

