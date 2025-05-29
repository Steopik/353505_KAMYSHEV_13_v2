from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from realty.views import about, faq_list, home, contact_list, privacy_policy, vacancy_list, promo_list
from realty.views import reviews_list, add_review,statistics


urlpatterns = [
    path('vacancies/', vacancy_list, name='vacancy_list'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('terms/', faq_list, name='faq_list'),
    path('contacts/', contact_list, name='contact_list'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('reviews/', reviews_list, name='reviews_list'),
    path('reviews/add/', add_review, name='add_review'),
    path('promocodes/', promo_list, name='promo_list'),
    path('accounts/', include('accounts.urls')),
    path('realty/', include('realty.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)