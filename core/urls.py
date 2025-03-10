from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('ranking/', views.ranking, name='ranking'),
    path('offer/<int:offer_id>/', views.specific_offer, name='specific_offer'),
]