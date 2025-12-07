from django.urls import path
from . import views


app_name = 'realty'

urlpatterns = [
    # Главная и статистика
    path('', views.home, name='home'),
    path('statistics/', views.statistics, name='statistics'),
    path('api/statistics/', views.statistics_api, name='statistics_api'),
    
    # CRUD для недвижимости
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:pk>/update/', views.property_update, name='property_update'),
    path('properties/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('properties/<int:pk>/buy/', views.buy_property, name='buy_property'),
    
    # Новости
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    
    # Информационные страницы
    path('about/', views.about, name='about'),
    path('faq/', views.faq_list, name='faq'),
    path('faq/<int:pk>/', views.faq_detail, name='faq_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.reviews, name='reviews'),
    path('promocodes/', views.promocodes, name='promocodes'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    
    # Корзина и оплата
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('payment/', views.payment_view, name='payment'),
    
    # API
    path('api/search/', views.api_property_search, name='api_property_search'),
    path('api/agents/', views.api_agents, name='api_agents'),
    path('api/properties/', views.api_properties, name='api_properties'),

    # JavaScript задания (ЛР3)
    path('js-tasks/', views.js_tasks, name='js_tasks'),
]