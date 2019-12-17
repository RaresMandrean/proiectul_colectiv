from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='eventix-home'),
    path('about/', views.about, name='eventix-about'),
]