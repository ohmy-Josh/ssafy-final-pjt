from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from movies.models import Movie, Actor, Director, Review
from packages.movies import youtube, naver
from ..models import Quiz, QuizPlay

@require_http_methods(['GET'])
def index(request):
    quizzes = Quiz.objects.all()
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'quizzes/single/index.html', context)


def quiz_index(request, quiz_pk):
    quiz = Quiz.objects.get(pk = quiz_pk)
    context = {
        'quiz': quiz,
    }
    return render(request, 'quizzes/single/quiz_index.html', context)


@require_http_methods(['POST', 'GET'])
def quiz_play(request, quiz_pk, quiz_num):
    quiz = Quiz.objects.get(pk = quiz_pk)
    user = request.user
    base_url = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/'

    if quiz_num == 0: 
        if request.method == 'POST':
            # 퀴즈 목록을 생성하자
            movies = Movie.objects.filter(original_language = 'ko')
            movies = movies.order_by('?')[:5]
            
            quiz_play = QuizPlay.objects.create(
                quiz = quiz,
                user = user,
                current  = 0,
            )
            for movie in movies:
                quiz_play.answer_list.add(movie)
            
            quiz_current = {
                'question' : quiz_play.answer_list.all().values_list(quiz.question)[quiz_play.current ][0],
                'answer' : quiz_play.answer_list.all().values_list(quiz.answer)[quiz_play.current][0]
            }    
        else:
            # method 오류
            return
    else:
        if quiz_num == 5:
            quiz_play =  QuizPlay.objects.get(quiz = quiz, user = user)
            quiz_play.delete()
            return redirect('quizzes:sin_index')

        quiz_play =  QuizPlay.objects.get(quiz = quiz, user = user)
        quiz_play.current = quiz_num
        quiz_play.save()
        quiz_current = {
                'question' : quiz_play.answer_list.all().values_list(quiz.question)[quiz_play.current][0],
                'answer' : quiz_play.answer_list.all().values_list(quiz.answer)[quiz_play.current][0]
            }

    context = {
                'base_url': base_url,
                'quiz_current': quiz_current,
                'quiz_pk': quiz_pk,
                'current': quiz_play.current + 1,
        }
    return render(request, 'quizzes/single/quiz.html', context)