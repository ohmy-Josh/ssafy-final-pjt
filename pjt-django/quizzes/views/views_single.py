from operator import length_hint
import random

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib.auth.decorators import login_required

from movies.models import Movie, Director
from ..models import Quiz, QuizPlay
from packages.movies import naver

@require_http_methods(['GET'])
def index(request):
    quizzes = Quiz.objects.all()
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'quizzes/single/index.html', context)


def quiz_index(request, quiz_pk):
    quiz = Quiz.objects.get(pk = quiz_pk)
    example = f'quiz-example/quiz{quiz_pk}_ex.jpg'
    context = {
        'quiz': quiz,
        'example': example, 
    }
    return render(request, 'quizzes/single/quiz_index.html', context)


@login_required
@require_http_methods(['POST', 'GET'])
def quiz_play(request, quiz_pk, quiz_num):
    quiz = Quiz.objects.get(pk = quiz_pk)
    user = request.user
    base_url = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2'

    if request.method == 'POST':
        if quiz_num == 0:
            # 퀴즈 목록을 생성하자
            if QuizPlay.objects.filter(quiz = quiz, user = user):
                quiz_play =  QuizPlay.objects.get(quiz = quiz, user = user)
                quiz_play.delete()

            quiz_play = QuizPlay.objects.create(
                quiz = quiz,
                user = user,
                current  = 0,
                result_list = [0]*10,
            )

            answers = Movie.objects.filter(original_language = 'ko').order_by('?')[:10]
            choices = []
            nums = 0
            while nums < 30:
                choice = Movie.objects.filter(original_language = 'ko').order_by('?')[0]
                if choice in answers or choice in choices:
                    continue
                choices.append(choice)
                nums += 1
    
            for answer in answers:
                quiz_play.answer_list.add(answer)
            for choice in choices:
                quiz_play.choice_list.add(choice)
            return redirect('quizzes:sin_quiz_play', quiz_pk, 1)

        else:
            if 'result' not in request.POST:
                # 답을 꼭 클릭하도록 메시지 띄우기
                return redirect('quizzes:sin_quiz_play', quiz_pk, quiz_num)
            
            result = request.POST['result']
            
            quiz_play =  QuizPlay.objects.get(quiz = quiz, user = user)
            
            quiz_play.result_list = quiz_grading(result, quiz_play, quiz_num, quiz.answer)
            quiz_play.save()
            return  redirect('quizzes:sin_quiz_play', quiz_pk, quiz_num + 1)

    else:
        if quiz_num > 10:

            return redirect('quizzes:sin_quiz_play_result', quiz_pk)

        quiz_play =  QuizPlay.objects.get(quiz = quiz, user = user)
        quiz_play.current = quiz_num
        quiz_play.save()

    choices = random.sample(quiz_choices(quiz_play, quiz, quiz_num), 4)

    quiz_current = {
            'question' : quiz_play.answer_list.all().values_list(quiz.question)[quiz_num-1][0],
            'choices' : choices,
            }
    
    context = {
                'base_url': base_url,
                'quiz_current': quiz_current,
                'quiz_pk': quiz_pk,
                'current': quiz_num,
        }
    page = f'quizzes/single/quiz{quiz_pk}.html'
    return render(request, page, context)


@login_required
@require_GET
def quiz_play_result(request, quiz_pk):
    quiz = Quiz.objects.get(pk = quiz_pk)
    user = request.user
    quiz_play =  QuizPlay.objects.get(quiz = quiz, user = user)
    results = quiz_play.result_list
    answers = quiz_play.answer_list.all()[::]
    corrects, incorrects = [], []
    
    for result, movie in zip(results, answers):
        if result:
            corrects.append(movie)
        else:
            incorrects.append(movie)
    score = len(corrects)*10
    context = {
        'corrects': corrects,
        'incorrects': incorrects,
        'quiz': quiz,
        'score': score,
    }

    return render(request, 'quizzes/single/quiz_result.html', context)


def quiz_grading(result, quiz_play, quiz_num, answer_field):
    answer = quiz_play.answer_list.all().values_list(answer_field)[quiz_num-1][0]
    if answer_field == 'directors':
        director = Director.objects.get(pk = answer)
        answer = director.name_kr
    correct = 1 if answer == result else 0
    results = quiz_play.result_list
    results[quiz_num-1] = correct
    return results


def quiz_choices(quiz_play, quiz, quiz_num):
    choices = [
        *quiz_play.choice_list.all().values_list(quiz.answer)[3*quiz_num-3:3*quiz_num], 
        quiz_play.answer_list.all().values_list(quiz.answer)[quiz_num-1]
        ]
    if quiz.answer ==  'directors':
        tmp = []
        for choice in choices:
            director = Director.objects.get(pk = choice[0])
            if director.name_kr == '':
                    director.name_kr = naver.papago(director.name, 'en', 'ko')['message']['result']['translatedText']
                    director.save()
            tmp.append(director.name_kr)
        choices = tmp

    return choices
