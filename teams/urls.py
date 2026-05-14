from django.urls import path
from . import views
urlpatterns = [
    path('', views.Team, name='teams'),
]


