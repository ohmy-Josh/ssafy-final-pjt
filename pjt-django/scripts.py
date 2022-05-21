from pprint import pprint
import requests
import json
from collections import OrderedDict
import urllib.request

# TMDB API 
TMDB_TOP_URL = 'https://api.themoviedb.org/3/movie/top_rated'
TMDB_API = '05331f044ea25f9c5d63cda187d08a2a'

# KMDB API 
KMDB_URL = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?'
KMDB_API = 'UM30MB478HW333CC5LPR'

# YOUTUBE API ('https://www.youtube.com/embed/' + video_id)
YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3/search'
YOUTUBE_API = 'AIzaSyAKwE_Pzl_CSP8wStqZYf4unklt9VH1IFc'

# NAVER API
NAVER_MOVIE_URL = 'https://openapi.naver.com/v1/search/movie.json'
NAVER_HEADERS = {
    'X-Naver-Client-Id': 'oaTKpVAjfWHNCp4akRpt',
    'X-Naver-Client-Secret': '5jKnOLvr7V',
}

def papago_translate(name):
    encText = urllib.parse.quote(name)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",NAVER_HEADERS['X-Naver-Client-Id'])
    request.add_header("X-Naver-Client-Secret",NAVER_HEADERS['X-Naver-Client-Secret'])
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        return response_body.decode('utf-8')
    else:
        return


# TMDB movie credit
def get_tmdb_top_rated_movie(page = 1):
    tmdb_data = []
    for i in range(1, page+1):
        tmdb_top_params = {
            'api_key' : TMDB_API, 
            'language' : 'ko-KR', 
            'page': i ,
        }
        tmdb_response = requests.get(TMDB_TOP_URL, params=tmdb_top_params)
        tmdb_data += tmdb_response.json()['results']

    return tmdb_data


# TMDB movie credit
def get_tmdb_movie_credit(movie_id):
    TMDB_CREDIT_URL = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
    tmdb_params = {
        'api_key' : TMDB_API, 
        'language' : 'ko-KR', 
    }
    tmdb_credit_response = requests.get(TMDB_CREDIT_URL, params=tmdb_params)
    credit = {
        'actors': tmdb_credit_response.json()['cast'],
        'directors': [crew for crew in tmdb_credit_response.json()['crew'] if crew['job']=='Director'],
    }
    return credit 


# KMDB credit
def kmdb_credit(movie):
    credit_kr = {
        'actors': {},
        'directors':  {},
    }

    if '"' in movie['title'] \
        or "'" in movie['title'] \
        or '!' in movie['title']:
        return credit_kr

    else:
        # KMDB   
        kmdb_params = {
            'collection': 'kmdb_new2',
            'ServiceKey': KMDB_API,
            'query' : movie['title'], 
            'detail' : 'Y',
            'createDts' : movie['release_date'][:4], 
            'createDte' : movie['release_date'][:4], 
        }
        kmdb_response = requests.get(KMDB_URL, params=kmdb_params)
        
        if 'Result' not in kmdb_response.json()['Data'][0]:
            return credit_kr

        actors_kr = kmdb_response.json()['Data'][0]['Result'][0]['actors']['actor']
        directors_kr = kmdb_response.json()['Data'][0]['Result'][0]['directors']['director']

        actors_kr = dict((actor['actorEnNm'], actor['actorNm']) for actor in actors_kr if actor.get('actorEnNm', ''))
        directors_kr = dict((director['directorEnNm'] if director['directorEnNm'] else idx, director['directorNm']) for idx, director in enumerate(directors_kr))

    credit_kr = {
        'actors': actors_kr,
        'directors':  directors_kr,
    }

    return credit_kr


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
            if key == 'directors' and not name_kr and len(credit_kr[key]) == 1:
                name_kr = list(credit_kr[key].values())[0]

            model_tmp['fields'] =  {
                'name': person['name'],
                'name_kr': name_kr,
                }
            models[key].append(model_tmp)

        pk_list.append(pk)

    return pk_list


def youtube_search_trailer(title, ko = True):
    trailer = '예고편' if ko else 'trailer'
    youtube_params = {
        'key' : YOUTUBE_API, 
        'part' : 'snippet', 
        'q' : title + trailer, 
    }

    youtube_response = requests.get(YOUTUBE_URL, params=youtube_params)
    videoId = youtube_response.json()['items'][0]['id']['videoId']

    return  videoId

def movie_process(movie, movie_pk):
    # movie object 생성
    model_movie = OrderedDict()
    
    model_movie['model'] = 'movies.movie'
    model_movie['pk'] = movie_pk
    model_movie['fields'] = {
            'title': movie['title'],
            'backdrop_path': movie['backdrop_path'],
            'poster_path': movie['poster_path'],
            'trailer_path': '', # youtube_search_trailer(movie['original_title'], ko = movie['original_language'] == 'ko'),
            'release_date': movie['release_date'],
            'vote_average': movie['vote_average'],
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

tmdb_movies = get_tmdb_top_rated_movie(page = 20)

for movie in tmdb_movies:
    if not movie['overview']:
        continue

    credit = get_tmdb_movie_credit(movie['id'])
    credit_kr = kmdb_credit(movie)

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