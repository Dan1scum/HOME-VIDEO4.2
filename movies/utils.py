from django.db.models import Q
from .models import Movie


def filter_movies(queryset, search_query=None, category_id=None, genre_ids=None, sort_by=None):
    """
    Фильтрация фильмов по различным критериям
    """
    if search_query:
        search_query = search_query.strip()
        if search_query:
            tokens = [t for t in search_query.split() if t]
            q_objects = Q()
            for token in tokens:
                q_objects &= Q(title__icontains=token) | Q(description__icontains=token)
            queryset = queryset.filter(q_objects)
    
    if category_id:
        try:
            queryset = queryset.filter(category__id=int(category_id))
        except (ValueError, TypeError):
            pass
    
    if genre_ids:
        queryset = queryset.filter(genres__id__in=genre_ids).distinct()
    
    if sort_by:
        valid_sorts = ['-created_at', 'created_at', 'title', '-title', '-rating', 'rating']
        if sort_by in valid_sorts:
            queryset = queryset.order_by(sort_by)
    
    return queryset


def get_movie_context(movie, user):
    """
    Получить контекст для фильма
    """
    return {
        'movie': movie,
        'is_author': movie.author == user if user.is_authenticated else False,
        'is_staff': user.is_staff if user.is_authenticated else False,
    }
