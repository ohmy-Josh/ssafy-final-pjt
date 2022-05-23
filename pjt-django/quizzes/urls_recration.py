from django.urls import path
from .views import views_recration

urlpatterns = [
    path('recration/', views_recration.index, name='rec_index'),
]
 