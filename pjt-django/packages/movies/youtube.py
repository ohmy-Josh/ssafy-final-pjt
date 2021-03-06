import requests
from . import API_keys as api

# YOUTUBE API ('https://www.youtube.com/embed/' + video_id)
YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3/search'
YOUTUBE_API = api.YOUTUBE_API

def youtube_search_trailer(title, ko = True):
    trailer = ' 예고편' if ko else ' trailer'
    youtube_params = {
        'key' : YOUTUBE_API, 
        'part' : 'snippet', 
        'q' : title + trailer, 
    }

    youtube_response = requests.get(YOUTUBE_URL, params=youtube_params)
    if youtube_response.status_code == 403:
        return ''

    videoId = youtube_response.json()['items'][0]['id']['videoId']
    return videoId 
