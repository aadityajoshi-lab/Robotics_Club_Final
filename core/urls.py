from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.Contact, name='contact'),
    path('resources/', views.Resources, name='resources'),
path('resource/<str:resource_type>/<int:pk>/', views.access_resource, name='access_resource'),]
