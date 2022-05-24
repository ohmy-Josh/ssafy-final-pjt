from django.db import models
from django.conf import settings
from movies.models import Movie

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

class QuizPlay(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer_list = models.ManyToManyField(Movie)
    current = models.IntegerField()
