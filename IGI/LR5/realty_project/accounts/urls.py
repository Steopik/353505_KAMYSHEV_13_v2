from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('confirm-email/<int:user_id>/', views.confirm_email, name='confirm_email'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/avatar/', views.update_avatar, name='update_avatar'),
]