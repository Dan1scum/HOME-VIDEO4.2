# FilmRoom Configuration

# Pagination
MOVIES_PER_PAGE = 12
USERS_PER_PAGE = 20

# File uploads
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

# Search
MIN_SEARCH_LENGTH = 2
MAX_SEARCH_LENGTH = 100

# Rating
MIN_RATING = 0
MAX_RATING = 10

# Cache
CACHE_TIMEOUT = 300  # 5 minutes

# Sorting options
MOVIE_SORT_OPTIONS = [
    ('-created_at', 'Newest'),
    ('created_at', 'Oldest'),
    ('-rating', 'Top Rated'),
    ('rating', 'Lowest Rated'),
    ('title', 'A-Z'),
    ('-title', 'Z-A'),
]

# Avatar sizes
AVATAR_SIZE = (200, 200)
POSTER_SIZE = (300, 450)
