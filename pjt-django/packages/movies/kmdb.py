import requests
from . import API_keys as api

# KMDB API 
KMDB_URL = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?'
KMDB_API = api.KMDB_API

def delete_tags(name):
    if '!' in name:
        tokens = name.split()
        tokens = [token for token in tokens if '!' not in token]
        result = ' '.join(tokens)
        return result
    else:
        return name
        
# KMDB credit
def kmdb_credit(movie):
    credit_kr = {
        'actors': {},
        'directors':  {},
    }
    query = movie['title']
    query = query.replace(';', '').replace('"', '').replace("'", '').replace('!', '')
    
    # KMDB   
    kmdb_params = {
        'collection': 'kmdb_new2',
        'ServiceKey': KMDB_API,
        'query' : query, 
        'detail' : 'Y',
        'createDts' : movie['release_date'][:4], 
        'createDte' : movie['release_date'][:4], 
    }
    kmdb_response = requests.get(KMDB_URL, params=kmdb_params)
    
    if 'Result' not in kmdb_response.json()['Data'][0]:
        return credit_kr

    actors_kr = kmdb_response.json()['Data'][0]['Result'][0]['actors']['actor']
    directors_kr = kmdb_response.json()['Data'][0]['Result'][0]['directors']['director']

    actors_kr = dict((actor['actorEnNm'], delete_tags(actor['actorNm'])) for actor in actors_kr if actor.get('actorEnNm', ''))
    directors_kr = dict((director['directorEnNm'], delete_tags(director['directorNm'])) for director in directors_kr if director.get('directorEnNm', ''))

    credit_kr = {
        'actors': actors_kr,
        'directors':  directors_kr,
    }

    return credit_kr