from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Category, Genre
from .forms import MovieForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.functions import Lower


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
    return render(request, 'movies/movie_detail.html', {'movie': movie})


@login_required
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, 'Movie created successfully')
            return redirect('movies:detail', pk=movie.pk)
    else:
        form = MovieForm()
    return render(request, 'movies/movie_create.html', {'form': form})


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
