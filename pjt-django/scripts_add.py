import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")

import django
django.setup()

from packages.movies import tmdb, kobis, kmdb
from movies.models import Movie, Actor, Director

# 조회할 top_rate page 설정 
movies = tmdb.get_tmdb_top_rated_movie(page = 30)

# 조회할 주간 박스오피스 기간 설정 : (start, end)
# ko_movies = kobis.kobis_boxoffice_traversal('20031101', '20061231')
# 2003 ~ 2022 반영
# movies += ko_movies
 
nums = len(movies)
print(f'{nums}편 영화 목록 추출 완료')
num = 0
for movie in movies:
    num += 1
    new_movie, created = Movie.objects.get_or_create(
        movie_id = movie['id'],
        defaults={
            'title': movie['title'],
            'original_title': movie['original_title'],
            'backdrop_path': movie['backdrop_path'] if movie['backdrop_path'] else '/',
            'poster_path': movie['poster_path'] if movie['poster_path'] else '/',
            'trailer_path': '', 
            'release_date': movie['release_date'],
            'vote_average': movie['vote_average'],
            'original_language': movie['original_language'],
            'overview': movie['overview'],
            })
    if not created:
        continue

    if not movie['overview']:
        continue
    
    credit = tmdb.get_tmdb_movie_credit(movie['id'])
    credit_kr = kmdb.kmdb_credit(movie)

    for person in credit['directors']:
        director, created = Director.objects.get_or_create(
            director_id = person['id'],
            defaults={
                'name': person['name'],
                'name_kr': credit_kr['directors'].get(person['name'], '')
                })
        director.movies.add(new_movie)

    for person in credit['actors']:
        actor, created = Actor.objects.get_or_create(
            actor_id = person['id'],
            defaults={
                'name': person['name'],
                'name_kr': credit_kr['actors'].get(person['name'], '')
                })
        actor.movies.add(new_movie)

    if num % 50 == 0:
        print(f'{num}번째 영화 입력 완료')