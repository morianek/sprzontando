from django.urls import path
from . import views

urlpatterns = [
path('users_with_low_reviews/', views.users_with_low_reviews, name='users_with_low_reviews'),
path('user_statistics/', views.user_statistics, name='user_statistics'),
path('reported_offers/', views.reported_offers, name='reported_offers'),
]