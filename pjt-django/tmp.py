import random

import os
from webbrowser import BackgroundBrowser
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")

import django
django.setup()

from movies.models import Movie, Actor, Director

movies = Movie.objects.filter(original_language = 'ko')
movies = movies.order_by('?')
answers = movies[:1]
print(answers)
