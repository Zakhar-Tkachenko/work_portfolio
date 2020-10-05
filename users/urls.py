from django import urls
from django.urls import path
from .models import Profile
from . import views

urlpatterns = [
    path('<slug:name>/', views.profile, name='profile'),
    path('', views.myprofile, name='my_profile')
]