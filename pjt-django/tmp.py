import random

import os
from webbrowser import BackgroundBrowser
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")

import django
django.setup()

from movies.models import Movie, Actor, Director

movies = Movie.objects.filter(original_language = 'ko')
movies = movies.order_by('?')[:5]

movie = Movie.objects.get(pk = 1)

print(movies.values_list('title')[0])