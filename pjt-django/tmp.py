import random

import os
from webbrowser import BackgroundBrowser
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")

import django
django.setup()

from movies.models import Movie, Actor, Director

import json

movie = Movie.objects.filter(title = '김씨 표류기')

with open(f'fixtures/movies/tmp.json', 'w', encoding="utf-8") as make_file:
        json.dump(movie, make_file, ensure_ascii=False, indent="\t")
