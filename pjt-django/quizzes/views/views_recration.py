from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from movies.models import Movie, Actor, Director, Review
from packages.movies import youtube, naver


@require_http_methods(['GET'])
def index(request):    
    return render(request, 'quizzes/recration/index.html')


