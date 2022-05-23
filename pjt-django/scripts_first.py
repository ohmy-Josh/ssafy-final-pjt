from packages.movies import tmdb, kobis, kmdb
import json
from collections import OrderedDict

def credit_process(key):

    pk_list = []
    for person in credit[key]:
        id = person['id']
        if id in models_dict[key]:
            pk = models_dict[key][id]
        else:
            models_dict[key]['num'] += 1
            pk = models_dict[key]['num']
            models_dict[key][id] = pk

            model_tmp = OrderedDict()
            model_tmp['model'] = f'movies.{key[:-1]}'
            model_tmp['pk'] = pk
            
            name_kr = credit_kr[key].get(person['name'], '')

            model_tmp['fields'] =  {
                f'{key[:-1]}_id': person['id'],
                'name': person['name'],
                'name_kr': name_kr,
                }
            models[key].append(model_tmp)

        pk_list.append(pk)

    return pk_list


def movie_process(movie, movie_pk):
    # movie object 생성
    model_movie = OrderedDict()
    
    model_movie['model'] = 'movies.movie'
    model_movie['pk'] = movie_pk
    model_movie['fields'] = {
            'movie_id': movie['id'],
            'title': movie['title'],
            'original_title': movie['original_title'],
            'backdrop_path': movie.get('backdrop_path', ''),
            'poster_path':movie.get('poster_path', ''),
            'trailer_path': '', # youtube_search_trailer(movie['original_title'], ko = movie['original_language'] == 'ko'),
            'release_date': movie['release_date'],
            'vote_average': movie.get('vote_average', ''),
            'original_language': movie['original_language'],
            'overview': movie['overview'],
            'directors': directors,
            'actors': actors,
    }

    models['movies'].append(model_movie)
    return

models = {
    'movies': [],
    'actors': [],
    'directors': [],}

models_dict = {
    'movies': 0,
    'actors': {'num': 0,},
    'directors': {'num': 0,},
}

# 조회할 주간 
movies = tmdb.get_tmdb_top_rated_movie(page = 1)

# 조회할 주간 박스오피스 기간 설정 : (start, end)
ko_movies = kobis.kobis_boxoffice_traversal('20150101', '20161231')

movies += ko_movies 

print(f'{len(movies)}편 영화 목록 추출 완료')
for movie in movies:
    if not movie['overview']:
        continue
    
    credit = tmdb.get_tmdb_movie_credit(movie['id'])
    credit_kr = kmdb.kmdb_credit(movie)


    actors = credit_process('actors')
    directors = credit_process('directors')

    models_dict['movies'] += 1
    movie_pk = models_dict['movies']
    movie_process(movie, movie_pk)

    if movie_pk % 50 == 0:
        print(f'{movie_pk}번째 영화 완료')

def write_json(key):
    with open(f'fixtures/movies/{key}.json', 'w', encoding="utf-8") as make_file:
        json.dump(models[key], make_file, ensure_ascii=False, indent="\t")

    print(f'{key} 모델 json 파일 생성 완료')
    return 

write_json('movies')
write_json('actors')
write_json('directors')

# python manage.py loaddata fixtures/movies/actors.json fixtures/movies/movies.json fixtures/movies/directors.json