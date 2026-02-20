from .models import Category, Genre, Movie


def categories(request):
    """Добавить все категории в контекст каждого шаблона"""
    return {
        'categories': Category.objects.all(),
        'genres': Genre.objects.all(),
        'popular_movies': Movie.objects.order_by('-rating')[:5],
    }


def site_config(request):
    """Добавить конфигурацию сайта в контекст"""
    return {
        'site_title': 'FilmRoom',
        'site_description': 'Discover and share your favorite movies',
        'version': '2.0',
    }
