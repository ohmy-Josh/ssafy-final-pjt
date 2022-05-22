import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")

import django
django.setup()

from packages.movies import naver
from movies.models import Movie, Actor, Director

# movie 모델 불러오기
# 한국 영화(original_language = ko) 검색
# 한국 영화 출연 배우, 감독(actor, director) 탐색
# name_kr이 비어있는 경우 파파고 번역 

movies = Movie.objects.filter(original_language = 'ko')
actors = Actor.objects.none()

for movie in movies:
    actors = movie.actors.filter(name_kr = "")

    for actor in actors:
        papago_response = naver.papago(actor.name, 'en', 'ko')
        name_kr = papago_response['message']['result']['translatedText']
        actor.name_kr = name_kr
        actor.save()

    directors = movie.directors.filter(name_kr = "")

    for director in directors:
        papago_response = naver.papago(director.name, 'en', 'ko')
        name_kr = papago_response['message']['result']['translatedText']
        director.name_kr = name_kr
        director.save()