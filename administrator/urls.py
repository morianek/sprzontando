from django.urls import path
from . import views

urlpatterns = [
path('users_with_low_reviews/', views.users_with_low_reviews, name='users_with_low_reviews'),
]