from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.my_offers, name='user_offers'),
]