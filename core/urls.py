from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('ranking/', views.ranking, name='ranking'),
    path('offer/<int:offer_id>/', views.specific_offer, name='specific_offer'),
    path('offer/<int:offer_id>/apply/', views.apply_for_offer, name='apply_for_offer'),
    path('offer/<int:offer_id>/cancel/', views.withdraw_application, name='withdraw_application'),
    path('offer/<int:offer_id>/report/', views.report_offer, name='report_offer'),
    path('offer/<int:offer_id>/ban', views.ban_offer, name='ban_offer'),
    path('specficic_user/<int:user_id>/', views.specific_user, name='specific_user'),
    path('ban_user/<int:user_id>/', views.ban_user, name='ban_user'),
]