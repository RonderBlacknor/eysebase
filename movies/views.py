from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404

from .models import Movie, Director



menu = [

    {'title': 'Главная', 'url_name': 'index'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить фильм', 'url_name': 'add_movie' },
]

def index(request):
    movies = Movie.objects.all
    param = {
        'menu': menu,
        'movies': movies,
        'title': 'Главная Страница'
    }
    return render(request, 'movies/index.html', context=param )

def about(request):
    movie_count = Movie.objects.filter(is_published=True).count()
    director_count = Director.objects.count()

    param = {
        'menu': menu,
        'title': 'О сайте', 
        'movie_count': movie_count,
        'director_count': director_count,
    }
    return render(request, 'movies/about.html', {'menu':menu, 'title': 'О сайте', 'movie_count': movie_count, 'director_count': director_count})

def movie_by_genre(request, genre_id): 
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genres=genre)

    param = {
        'menu': menu, 
        'movie': movies, 
        'title': f'Фильмы в жанре: {genre.name}'
    }
    
def genre(request, genreid):
    print(request.GET)
    return HttpResponse(f'<h1> Жанры фильмов </h1> <p>{genreid}</p>')

def movies(request, year):
    if int(year) > 2025:
        return redirect('/', permanent=True)
    return HttpResponse(f'Фильмы за {year}г.')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страницы не сущетсвует</h1>')

def show_movie(request, post_id): 
    movie = get_object_or_404(Movie, pk=post_id)
    param = {
        'menu': menu, 
        'title': movie.title, 
        'movie': movie
    }

    return render(request, 'movies/movie_detail.html', context=param)


def add_movie(request):
    return HttpResponse('Добавление фильма')

def show_director(requet, post_id): 
    return HttpResponse(f'Страница директора с ID = {post_id}')

#site.ru/?movie=tenet&year=2020 - пример