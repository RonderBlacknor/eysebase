from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Director(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="directors/%Y/%m/%d", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('director', kwargs={'director_id': self.pk})

class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(blank=True, null=True)
    poster = models.ImageField(upload_to="posters/%Y/%m/%d", blank=True, null=True)
    release_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)], 
        null=True, 
        blank=True
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], 
        default=0.0, 
        blank=True, 
        null=True
    )
    director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True, related_name='directed_movies')
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

class Watchlist(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')
    watched_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta: 
        unique_together = ('user', 'movie')
        verbose_name = 'Список Просмотренного'
        verbose_name_plural = 'Списки просмотренного'

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'