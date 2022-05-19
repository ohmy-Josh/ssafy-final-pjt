import requests
import json
from collections import OrderedDict

# TMDB API 
TMDB_TOP_URL = 'https://api.themoviedb.org/3/movie/top_rated'
TMDB_API = ''

# NAVER API
NAVER_MOVIE_URL = 'https://openapi.naver.com/v1/search/movie.json'
NAVER_HEADERS = {
    'X-Naver-Client-Id': '',
    'X-Naver-Client-Secret': '',
}

model_movies = []
model_directors = []
model_actors = []
actors_dict = { 'dict_length': 0, }
directors_dict = { 'dict_length': 0,}
movies_num = 0

tmdb_data = []

for i in range(1, 51): # 20 * 50 page
    tmdb_params = {
        'api_key' : TMDB_API, 
        'language' : 'ko-KR', 
        'page' : i, 
    }

    tmdb_response = requests.get(TMDB_TOP_URL, params=tmdb_params)
    tmdb_data += tmdb_response.json()['results']

for movie in tmdb_data:
    # TMDB CREDIT
    movie_id = movie['id']
    TMDB_CREDIT_URL = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
    response = requests.get(TMDB_CREDIT_URL, params=tmdb_params)
    
    # actor object 확인 후 추가
    actors = []    
    for cast in response.json()['cast']:
        actor_id = cast['id']
        if actor_id in actors_dict:
            actor_pk = actors_dict[actor_id]
        else:
            actors_dict['dict_length'] += 1
            actor_pk = actors_dict['dict_length']
            actors_dict[actor_id] = actor_pk
            model_actor = OrderedDict()
            model_actor['model'] = 'movies.actor'
            model_actor['pk'] = actor_pk
            model_actor['fields'] =  {'name': cast['name'],}
            model_actors.append(model_actor)

        actors.append(actor_pk)

    # director object 확인 후 추가
    directors = []
    for crew in response.json()['crew']:
        if crew['job'] == 'Director':
            director_id = crew['id']
            if director_id in directors_dict:
                director_pk = directors_dict[director_id]
            else:
                directors_dict['dict_length'] += 1
                director_pk = directors_dict['dict_length']
                directors_dict[director_id] = director_pk
                model_director = OrderedDict()
                model_director['model'] = 'movies.director'
                model_director['pk'] = int(director_pk)
                model_director['fields'] =  {'name': crew['name'],}
                model_directors.append(model_director)

            directors.append(director_pk)
    
    # NAVER searcj > movie    
    naver_params = {
        'query' : movie['title'], 
        'yearfrom' : movie['release_date'][:4], 
        'yearto' : movie['release_date'][:4], 
    }
    
    naver_response = requests.get(NAVER_MOVIE_URL, headers = NAVER_HEADERS, params=naver_params)
    
    if not naver_response.json()['items']:
        continue
    naver_data = naver_response.json()['items'][0]
    directors_kr = ', '.join(list(a for a in naver_data['director'].split('|') if a))
    actors_kr = ', '.join(list(a for a in naver_data['actor'].split('|') if a))

    movies_num += 1
    
    # movie object 생성
    model_movie = OrderedDict()
    
    model_movie['model'] = 'movies.movie'
    model_movie['pk'] = movies_num
    model_movie['fields'] = {
            'title': movie['title'],
            'overview': movie['overview'],
            'backdrop_path': movie['backdrop_path'],
            'poster_path': movie['poster_path'],
            'release_date': movie['release_date'],
            'vote_average': movie['vote_average'],
            'directors': directors,
            'actors': actors,
            'directors_kr': directors_kr,
            'actors_kr': actors_kr,
            'userRating': naver_data['userRating'],
    }

    model_movies.append(model_movie)
    if movies_num % 50 == 0:
        print(f'{movies_num}번째 영화')

# Write JSON
with open('fixtures/movies/movies.json', 'w', encoding="utf-8") as make_file:
    json.dump(model_movies, make_file, ensure_ascii=False, indent="\t")

with open('fixtures/movies/actors.json', 'w', encoding="utf-8") as make_file:
    json.dump(model_actors, make_file, ensure_ascii=False, indent="\t")

with open('fixtures/movies/directors.json', 'w', encoding="utf-8") as make_file:
    json.dump(model_directors, make_file, ensure_ascii=False, indent="\t")

# python manage.py loaddata fixtures/movies/actors.json fixtures/movies/movies.json fixtures/movies/directors.json