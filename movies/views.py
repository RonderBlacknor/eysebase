from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Movie, Director, Genre, Watchlist

menu = [

    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить фильм', 'url_name': 'add_movie' },
    {'title': 'Регистрация', 'url_name': 'register' },
    {'title': 'Войти', 'url_name': 'login' },
    {'title': 'Выйти', 'url_name': 'logout' },
]

def logout_user(request):
    logout(request)
    return redirect('home')

def index(request):
    movies = Movie.objects.order_by('time_create').select_related('director').all()[:3]
    genres = Genre.objects.all()

    param = {
        'menu': menu,
        'movies': movies,
        'genres': genres,
        'title': 'Главная Страница'
    }
    return render(request, 'movies/index.html', context=param )

def all_movies(request):
    movies = Movie.objects.order_by('-time_create').select_related('director').all()

    param = {
        'menu': menu,
        'movies': movies,
        'title': 'Все фильмы'
    }
    return render(request, 'movies/all_movies.html', context=param )

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

def genre(request, genreid):
    print(request.GET)
    return HttpResponse(f'<h1> Жанры фильмов </h1> <p>{genreid}</p>')

def movies(request, year):
    if int(year) > 2025:
        return redirect('/', permanent=True)
    return HttpResponse(f'Фильмы за {year}г.')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm

    param = {
        'menu': menu,
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'movies/register.html', context=param)

@login_required
def add_to_watchlist(request, movie_id): 
    movie = get_object_or_404(Movie, pk=movie_id)
    Watchlist.objects.get_or_create(user=request.user, movie=movie)
    return redirect('post', post_id=movie-id)

@login_required
def profile(request):
    watchlist = Watchlist.objects.filter(user=request.user).select_related('movie')

    param = {
        'title': f'Профиль: {request.user.username}',
        'watchlist': watchlist
    }
    return render(request, 'movies/profile.html', context=param)

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

def movie_by_genre(request, genre_id): 
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genres=genre)

    param = {
        'menu': menu, 
        'movie': movies, 
        'title': f'Фильмы в жанре: {genre.name}'
    }

    return render(request, 'movies/movies_by_category.html', context=param)

def login_user(request): 
     
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    param = {
        'menu': menu,
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'movies/login.html', context=param)



#site.ru/?movie=tenet&year=2020 - пример