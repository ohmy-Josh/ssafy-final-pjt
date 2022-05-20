from django.db import models
from django.conf import settings

# Create your models here.
class Actor(models.Model):
    name = models.CharField(max_length=100)
    name_kr = models.CharField(max_length=100)


class Director(models.Model):
    name = models.CharField(max_length=100)
    name_kr = models.CharField(max_length=100)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    backdrop_path = models.CharField(max_length=30)
    poster_path = models.CharField(max_length=30)
    trailer_path =  models.CharField(max_length=30)
    release_date = models.DateField()
    vote_average = models.FloatField()
    overview = models.TextField()
    directors = models.ManyToManyField(Director, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')


class Review(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_pk = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)