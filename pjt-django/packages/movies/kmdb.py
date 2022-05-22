import requests

# KMDB API 
KMDB_URL = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?'
KMDB_API = 'UM30MB478HW333CC5LPR'


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

