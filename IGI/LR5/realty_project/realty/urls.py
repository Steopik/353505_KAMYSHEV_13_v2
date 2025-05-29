from django.urls import path
from . import views


app_name = 'realty'

urlpatterns = [
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:pk>/buy/', views.buy_property, name='buy_property'),
    path('statistics/', views.statistics, name='statistics'),
]