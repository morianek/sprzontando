from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.my_offers, name='user_offers'),
    path('add_offer/', views.add_offer, name='add_offer'),
]