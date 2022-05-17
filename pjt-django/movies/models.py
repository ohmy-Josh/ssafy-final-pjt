from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    backdrop_path = models.URLField()
    poster_path = models.URLField()
    release_date = models.DateField()
    vote_average = models.FloatField()
    genres = models.CharField(max_length = 10)
    director = models.CharField(max_length = 20)
    actors = models.CharField(max_length = 20)


class Review(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_pk = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)