from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Category
from .forms import MovieForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def movie_list(request):
	qs = Movie.objects.all().order_by('-created_at')
	q = request.GET.get('q')
	cat = request.GET.get('category')
	if q:
		qs = qs.filter(title__icontains=q)
	if cat:
		qs = qs.filter(category__id=cat)
	return render(request, 'movies/movie_list.html', {'movies': qs})


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
