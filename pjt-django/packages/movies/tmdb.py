import requests

# TMDB API 
TMDB_TOP_URL = 'https://api.themoviedb.org/3/movie/top_rated'
TMDB_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
TMDB_API = '05331f044ea25f9c5d63cda187d08a2a'

# TMDB movie top_rated
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


# TMDB search movie
def search_tmdb_movie(movieNm, openDt):
    tmdb_data = {}
    tmdb_search_params = {
        'api_key' : TMDB_API, 
        'language' : 'ko-KR', 
        'query': movieNm,
        'year': openDt[:4],
    }
    tmdb_response = requests.get(TMDB_SEARCH_URL, params=tmdb_search_params)
    if tmdb_response.json()['results']:
        tmdb_data = tmdb_response.json()['results'][0]

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

    