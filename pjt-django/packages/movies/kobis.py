import requests
from datetime import datetime, timedelta 
from . import tmdb

# KOBIS API
KOBIS_URL = 'https://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
KOBIS_API = '98217f55c5f31d1fc019c4a3c2ebe0a6'


def kobis_get_weekly_boxoffice(date):
    kobis_params = {
        'key': KOBIS_API, 
        'targetDt': date,
        'weekGb': 0,
        'itemPerPage': 3,
        'repNationCd': 'K', 
    }
    kobis_response = requests.get(KOBIS_URL, params=kobis_params)
    kobis_weekly_data = kobis_response.json()['boxOfficeResult']['weeklyBoxOfficeList']
    
    return kobis_weekly_data

def kobis_boxoffice_traversal(start, last):
    start_date = datetime.strptime(start, "%Y%m%d") 
    last_date = datetime.strptime(last, "%Y%m%d") 
    # 종료일 까지 반복 
    quiz_movies  = {}
    while start_date <= last_date: 
        dates = start_date.strftime("%Y%m%d") 
        weekly_movies = kobis_get_weekly_boxoffice(dates)
        for movie in weekly_movies:
            if movie['movieCd'] not in quiz_movies and int(movie['audiAcc']) >= 2000000:
                quiz_movies[movie['movieCd']] = ((movie['movieNm'], movie['openDt']))

        start_date += timedelta(days=7)

    movies = []
    for ko_movie in quiz_movies.values():
        movieNm, openDt = ko_movie
        search_movie = tmdb.search_tmdb_movie(movieNm, openDt)

        if search_movie:
            movies.append(search_movie)

    return movies
