from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('settings/user/', views.user_settings, name='user_settings'),
    path('settings/site/', views.site_settings, name='site_settings'),
]