from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .models import Movie, Actor, Director, Review
from .forms import ReviewForm
from packages.movies import youtube, naver

def get_trailers(movies):
    for movie in movies:
        if movie.trailer_path == '':
            movie.trailer_path = youtube.youtube_search_trailer(movie.original_title, movie.original_language == 'ko')
            movie.save()
    return

def get_name_kr(names):
    for name in names:
        if name.name_kr == '':
            name.name_kr = naver.papago(name.name, 'en', 'ko')['message']['result']['translatedText']
            name.save()
    return


@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        # 관리자만 접근 가능 + 새로운 영화 목록 추가
        return
    else:
        movies = Movie.objects.filter(pk__lte = 12)     # 반환할 movie list 수정 필요
        get_trailers(movies)

    context = {
        'movies': movies,
    }
    
    return render(request, 'movies/index.html', context)


@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    
    actors = movie.actors.all()[:5]
    directors = movie.directors.all()[:2]
    reviews = movie.review_set.all()

    actor_movies, director_movies = Movie.objects.none(), Movie.objects.none()
    # 관련 영화에서 detail 영화는 제거하기
    for actor in actors:
        actor_movies |= actor.movies.all()
    for director in directors:
        director_movies |= director.movies.all()
    
    actor_movies = actor_movies.exclude(pk = movie_pk).distinct()
    director_movies = director_movies.exclude(pk = movie_pk).distinct()
    
    get_trailers(actor_movies)
    get_trailers(director_movies)

    if movie.original_language == 'ko':
        get_name_kr(actors)
        get_name_kr(directors)

    form = ReviewForm()

    context = {
        'movie': movie,
        'actors': actors,
        'directors': directors,
        'actor_movies': actor_movies,
        'director_movies': director_movies,
        'reviews': reviews,
        'review_form': form,
    }
        
    return render(request, 'movies/detail.html', context)


@require_POST
def create_review(request, movie_pk):
    # 로그인한 사용자만 접근하도록 허용하기

    movie = get_object_or_404(Movie, pk=movie_pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.movie = movie
        review.user = request.user
        review.save()
    return redirect('movies:detail', movie.pk)


# review 수정 및 삭제 구현