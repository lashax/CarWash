from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('washers/', views.washers, name='washers'),
    path('cars/', views.cars, name='cars')
]
