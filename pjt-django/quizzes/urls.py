from django.urls import path
from django.urls import URLPattern
from . import urls_single
from . import urls_recration
from .views import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += urls_single.urlpatterns
urlpatterns += urls_recration.urlpatterns
