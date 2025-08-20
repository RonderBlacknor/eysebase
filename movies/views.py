from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import Movie



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
    return render(request, 'movies/about.html', {'menu':menu, 'title': 'О сайте'})

def genre(request, genreid):
    print(request.GET)
    return HttpResponse(f'<h1> Жанры фильмов </h1> <p>{genreid}</p>')

def movies(request, year):
    if int(year) > 2025:
        return redirect('/', permanent=True)
    return HttpResponse(f'Фильмы за {year}г.')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страницы не сущетсвует</h1>')

def show_movie(requet, post_id): 
    return HttpResponse(f'Страница Фильма с ID = {post_id}')
def add_movie(request):
    return HttpResponse('Добавление фильма')

def show_director(requet, post_id): 
    return HttpResponse(f'Страница директора с ID = {post_id}')

#site.ru/?movie=tenet&year=2020 - пример