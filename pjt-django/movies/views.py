from django.shortcuts import render



# Create your views here.
def index(request):
    movies = []
    context = {
        'movies': movies,
    }
    return render (request, 'movies/index.html', context)
