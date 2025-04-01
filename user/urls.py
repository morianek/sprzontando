from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.my_offers, name='user_offers'),
    path('add_offer/', views.add_offer, name='add_offer'),
    path('offer/<int:offer_id>/', views.edit_specific_offer, name='user_edit_specific_offer'),
    path('offer/<int:offer_id>/choose_applicants/', views.choose_applicants, name='choose_applicants'),
]