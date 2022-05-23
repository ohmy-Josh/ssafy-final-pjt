import random

import os
from webbrowser import BackgroundBrowser
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")

import django
django.setup()

from movies.models import Movie, Actor, Director

movies = Movie.objects.filter(original_language = 'ko')
movies = movies.order_by('?')[:5]

POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/'
quiz_list = [{'question':q[0], 'answer':a[0]}for q, a in zip(movies.values_list('backdrop_path'), movies.values_list('title'))]

print(quiz_list)
