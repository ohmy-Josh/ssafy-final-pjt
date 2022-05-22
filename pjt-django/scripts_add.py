import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_pjt.settings")

import django
django.setup()

from collections import OrderedDict

from packages.movies import tmdb, kobis, kmdb
from movies.models import Movie, Actor, Director
import scripts_first as script


# 관련 함수 구현 필요