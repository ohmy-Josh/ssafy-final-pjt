from django.urls import path
from .views import views_single

urlpatterns = [
    path('single/', views_single.index, name='sin_index'),
    path('single/<int:quiz_pk>/', views_single.quiz_index, name='sin_quiz_index'),
    path('single/<int:quiz_pk>/<int:quiz_num>/', views_single.quiz_play, name='sin_quiz_play'),

]
 