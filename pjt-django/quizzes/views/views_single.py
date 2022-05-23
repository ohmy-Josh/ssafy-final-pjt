from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from movies.models import Movie, Actor, Director, Review
from packages.movies import youtube, naver
from packages.quizzes import quiz_list as Q

@require_http_methods(['GET'])
def index(request):
    context = {
        'quiz_list': Q.quiz_list.values(),
    }
    return render(request, 'quizzes/single/index.html', context)


def quiz_index(request, quiz_num):
    quiz = Q.quiz_list.get(quiz_num, {})
    
    context = {
        'quiz': quiz,
    }
    return render(request, 'quizzes/single/quiz_index.html', context)


@require_http_methods(['GET'])
def quiz_play(request, quiz_num):
    quiz = Q.quiz_list.get(quiz_num, {})
    
    movies = Movie.objects.filter(original_language = 'ko')
    movies = movies.order_by('?')[:5]
    
    quiz_list = [
        {'question':q[0], 'answer':a[0]} 
        for q, a in zip(
            movies.values_list(quiz['question']), 
            movies.values_list(quiz['answer'])
            )]
    
    base_url = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/'
    context = {
        'quiz_list': quiz_list,
        'base_url': base_url,
    }

    return render(request, 'quizzes/single/quiz.html', context)