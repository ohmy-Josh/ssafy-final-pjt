from django.db import models
from django.conf import settings

# Create your models here.
class Actor(models.Model):
    name = models.CharField(max_length=100)


class Director(models.Model):
    name = models.CharField(max_length=100)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    backdrop_path = models.URLField()
    poster_path = models.URLField()
    release_date = models.DateField()
    vote_average = models.FloatField()
    directors = models.ManyToManyField(Director, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')
    directors_kr = models.CharField(max_length=100)
    actors_kr = models.CharField(max_length=100)
    userRating = models.FloatField()


class Review(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_pk = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)