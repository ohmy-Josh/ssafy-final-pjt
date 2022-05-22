import urllib.request
import json

# NAVER API
NAVER_MOVIE_URL = 'https://openapi.naver.com/v1/search/movie.json'
NAVER_HEADERS = {
    'X-Naver-Client-Id': 'oaTKpVAjfWHNCp4akRpt',
    'X-Naver-Client-Secret': '5jKnOLvr7V',
}

def papago(name, fr , to):
    encText = urllib.parse.quote(name)
    data = f"source={fr}&target={to}&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",NAVER_HEADERS['X-Naver-Client-Id'])
    request.add_header("X-Naver-Client-Secret",NAVER_HEADERS['X-Naver-Client-Secret'])
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    
    if(rescode==200):
        response_body = response.read()
        response_query = response_body.decode("utf-8")
        return json.loads(response_query)

    else:
        return
