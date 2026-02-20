from django import template

register = template.Library()


@register.filter
def star_rating(value):
    try:
        value = float(value)
        stars = int(value)
        return '⭐' * stars
    except (ValueError, TypeError):
        return ''


@register.filter
def truncate_words(value, words=10):
    if not value:
        return ''
    words_list = str(value).split()
    if len(words_list) > words:
        return ' '.join(words_list[:words]) + '...'
    return value


@register.simple_tag
def get_genre_count(movie):
    return movie.genres.count()


@register.simple_tag
def get_movie_count_by_author(author):
    return author.movies.count()
