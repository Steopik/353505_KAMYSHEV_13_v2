from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, Sum
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
import pytz
from datetime import datetime, date
import calendar
from decimal import Decimal

from .models import (
    Property, Buyer, Sale, Agent, CompanyInfo, FAQ,
    Vacancy, Review, PromoCode, News, Owner, Partner
)
from .forms import ReviewForm
from .statistics import RealtyStatistics
from .api_services import CurrencyService, WeatherService, IPGeolocationService


def is_superuser(user):
    return user.is_superuser


def home(request):
    """Главная страница с последней новостью и статистикой"""
    latest_news = News.objects.filter(is_published=True).first()
    featured_properties = Property.objects.filter(is_available=True).order_by('-created_at')[:6]
    
    # Получаем погоду и курсы валют
    weather = WeatherService.get_minsk_weather()
    usd_rate = CurrencyService.get_usd_rate()
    eur_rate = CurrencyService.get_eur_rate()
    
    # Получаем IP и местоположение пользователя
    client_ip = request.META.get('REMOTE_ADDR')
    location = IPGeolocationService.get_location_by_ip(client_ip)
    
    # Timezone пользователя
    user_timezone = pytz.timezone(location['timezone']) if location['timezone'] else pytz.UTC
    current_time = datetime.now(user_timezone)
    
    # Календарь текущего месяца
    cal = calendar.HTMLCalendar()
    calendar_html = cal.formatmonth(current_time.year, current_time.month)

    # Получаем партнеров из БД
    partners = Partner.objects.filter(is_active=True).order_by('order', 'name')

    context = {
        'latest_news': latest_news,
        'featured_properties': featured_properties,
        'weather': weather,
        'usd_rate': float(usd_rate),
        'eur_rate': float(eur_rate),
        'location': location,
        'current_time': current_time,
        'utc_time': datetime.now(pytz.UTC),
        'calendar_html': calendar_html,
        'partners': partners,
    }
    
    return render(request, 'realty/home.html', context)


def property_list(request):
    """Список объектов недвижимости с поиском и сортировкой"""
    properties = Property.objects.filter(is_available=True)
    
    # Поиск
    query = request.GET.get('q', '')
    if query:
        properties = properties.filter(
            Q(title__icontains=query) | 
            Q(address__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Фильтр по типу
    property_type = request.GET.get('type', '')
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    # Фильтр по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['price', '-price', 'area', '-area', 'created_at', '-created_at']:
        properties = properties.order_by(sort_by)
    
    # Пагинация
    paginator = Paginator(properties, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Конвертация цен в валюты
    for prop in page_obj:
        prop.price_usd = CurrencyService.convert_to_usd(prop.price)
        prop.price_eur = CurrencyService.convert_to_eur(prop.price)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'property_type': property_type,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'types': Property.PROPERTY_TYPES,
    }
    
    return render(request, 'realty/property_list.html', context)


def property_detail(request, pk):
    """Детальная информация об объекте"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Конвертация цен
    property_obj.price_usd = CurrencyService.convert_to_usd(property_obj.price)
    property_obj.price_eur = CurrencyService.convert_to_eur(property_obj.price)
    
    # Связанные новости
    related_news = property_obj.news.filter(is_published=True)[:3]
    
    # Похожие объекты
    similar_properties = Property.objects.filter(
        property_type=property_obj.property_type,
        is_available=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'property': property_obj,
        'related_news': related_news,
        'similar_properties': similar_properties,
    }
    
    return render(request, 'realty/property_detail.html', context)


@login_required
def property_create(request):
    """Создание нового объекта недвижимости"""
    if request.method == 'POST':
        # Создание объекта из формы
        property_obj = Property(
            title=request.POST.get('title'),
            property_type=request.POST.get('property_type'),
            address=request.POST.get('address'),
            price=request.POST.get('price'),
            area=request.POST.get('area'),
            description=request.POST.get('description'),
            owner=request.user,
            is_available=True
        )
        property_obj.save()
        messages.success(request, 'Объект недвижимости успешно создан!')
        return redirect('realty:property_detail', pk=property_obj.pk)
    
    return render(request, 'realty/property_form.html', {
        'types': Property.PROPERTY_TYPES,
        'action': 'Создать'
    })


@login_required
def property_update(request, pk):
    """Редактирование объекта недвижимости"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Проверка прав
    if property_obj.owner != request.user and not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для редактирования этого объекта')
        return redirect('realty:property_detail', pk=pk)
    
    if request.method == 'POST':
        property_obj.title = request.POST.get('title')
        property_obj.property_type = request.POST.get('property_type')
        property_obj.address = request.POST.get('address')
        property_obj.price = request.POST.get('price')
        property_obj.area = request.POST.get('area')
        property_obj.description = request.POST.get('description')
        property_obj.save()
        messages.success(request, 'Объект недвижимости успешно обновлен!')
        return redirect('realty:property_detail', pk=property_obj.pk)
    
    return render(request, 'realty/property_form.html', {
        'property': property_obj,
        'types': Property.PROPERTY_TYPES,
        'action': 'Обновить'
    })


@login_required
def property_delete(request, pk):
    """Удаление объекта недвижимости"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Проверка прав
    if property_obj.owner != request.user and not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для удаления этого объекта')
        return redirect('realty:property_detail', pk=pk)
    
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Объект недвижимости успешно удален!')
        return redirect('realty:property_list')
    
    return render(request, 'realty/property_confirm_delete.html', {'property': property_obj})


def statistics(request):
    """Страница со статистикой"""
    stats = {
        'properties': RealtyStatistics.get_properties_statistics(),
        'sales': RealtyStatistics.get_sales_statistics(),
        'buyers': RealtyStatistics.get_buyer_statistics(),
        'reviews': RealtyStatistics.get_review_statistics(),
        'charts': RealtyStatistics.get_chart_data(),
        'most_profitable': RealtyStatistics.get_most_profitable_type(),
    }
    
    # Текущее время в разных форматах
    now = datetime.now()
    stats['current_date'] = {
        'local': now.strftime('%d/%m/%Y %H:%M:%S'),
        'utc': datetime.now(pytz.UTC).strftime('%d/%m/%Y %H:%M:%S UTC'),
        'iso': now.isoformat(),
    }
    
    return render(request, 'realty/statistics.html', stats)


def statistics_api(request):
    """API для получения данных статистики в JSON"""
    chart_data = RealtyStatistics.get_chart_data()
    return JsonResponse(chart_data)


def news_list(request):
    """Список новостей"""
    news = News.objects.filter(is_published=True).order_by('-published_at')
    
    # Поиск
    query = request.GET.get('q', '')
    if query:
        news = news.filter(
            Q(title__icontains=query) | 
            Q(brief__icontains=query) |
            Q(content__icontains=query)
        )
    
    paginator = Paginator(news, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'realty/news_list.html', {
        'page_obj': page_obj,
        'query': query,
    })


def news_detail(request, pk):
    """Детальная страница новости"""
    news_item = get_object_or_404(News, pk=pk)
    
    # Увеличиваем счетчик просмотров
    news_item.views_count += 1
    news_item.save(update_fields=['views_count'])
    
    return render(request, 'realty/news_detail.html', {'news': news_item})


def about(request):
    """Страница о компании"""
    company_info = CompanyInfo.objects.first()
    agents = Agent.objects.filter(is_active=True)
    
    return render(request, 'realty/about.html', {
        'company': company_info,
        'agents': agents,
    })




def contacts(request):
    """Страница контактов"""
    company_info = CompanyInfo.objects.first()
    agents = Agent.objects.filter(is_active=True)
    
    # Форматирование телефонов
    for agent in agents:
        if hasattr(agent, 'phone'):
            # Телефон уже в нужном формате благодаря валидатору
            pass
    
    return render(request, 'realty/contacts.html', {
        'company': company_info,
        'agents': agents,
    })


def vacancies(request):
    """Страница вакансий"""
    vacancies_list = Vacancy.objects.filter(is_published=True).order_by('-published_at')
    
    return render(request, 'realty/vacancies.html', {'vacancies': vacancies_list})


def reviews(request):
    """Страница отзывов"""
    reviews_list = Review.objects.all().order_by('-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('realty:reviews')
    else:
        form = ReviewForm() if request.user.is_authenticated else None
    
    # Статистика отзывов
    avg_rating = reviews_list.aggregate(Avg('rating'))['rating__avg'] or 0
    
    return render(request, 'realty/reviews.html', {
        'reviews': reviews_list,
        'form': form,
        'avg_rating': round(avg_rating, 1),
    })


def promocodes(request):
    """Страница промокодов"""
    active_promos = PromoCode.objects.filter(is_active=True)
    archived_promos = PromoCode.objects.filter(is_active=False)
    
    # Проверка возможности использования
    for promo in active_promos:
        promo.can_be_used = promo.can_use()
    
    return render(request, 'realty/promocodes.html', {
        'active_promos': active_promos,
        'archived_promos': archived_promos,
    })


def privacy_policy(request):
    """Страница политики конфиденциальности"""
    return render(request, 'realty/privacy_policy.html')


@login_required
def buy_property(request, pk):
    """Покупка недвижимости"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if not property_obj.is_available:
        messages.error(request, 'Этот объект уже продан')
        return redirect('realty:property_detail', pk=pk)
    
    # Проверяем, есть ли у пользователя профиль покупателя
    try:
        buyer = request.user.buyer_profile
    except:
        messages.error(request, 'Для покупки необходимо создать профиль покупателя')
        return redirect('realty:property_detail', pk=pk)
    
    if request.method == 'POST':
        promo_code = request.POST.get('promo_code', '')
        discount = 0
        
        # Проверка промокода
        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code)
                if promo.can_use():
                    discount = promo.discount_percent
                    promo.used_count += 1
                    promo.save()
                else:
                    messages.warning(request, 'Промокод недействителен')
            except PromoCode.DoesNotExist:
                messages.warning(request, 'Промокод не найден')
        
        # Создание продажи
        final_price = property_obj.price * Decimal(1 - discount / 100)
        
        sale = Sale.objects.create(
            property=property_obj,
            buyer=buyer,
            contract_number=f"SALE-{datetime.now().strftime('%Y%m%d')}-{property_obj.pk}",
            price_with_discount=final_price,
            agent=property_obj.agent
        )
        
        # Помечаем объект как проданный
        property_obj.is_available = False
        property_obj.save()
        
        messages.success(request, f'Поздравляем с покупкой! Номер договора: {sale.contract_number}')
        return redirect('realty:home')
    
    # Получаем доступные промокоды
    available_promos = PromoCode.objects.filter(is_active=True)
    
    return render(request, 'realty/buy_property.html', {
        'property': property_obj,
        'available_promos': available_promos,
    })


# API endpoints для AJAX запросов
def api_property_search(request):
    """API для поиска объектов"""
    query = request.GET.get('q', '')
    properties = Property.objects.filter(
        Q(title__icontains=query) | Q(address__icontains=query),
        is_available=True
    )[:10]
    
    data = [{
        'id': p.id,
        'title': p.title,
        'price': float(p.price),
        'address': p.address,
        'type': p.get_property_type_display()
    } for p in properties]
    
    return JsonResponse({'results': data})


# Представления для корзины покупок
def cart_view(request):
    """Страница корзины покупок"""
    # Получаем корзину из сессии
    cart = request.session.get('cart', {})
    
    # Получаем объекты недвижимости из корзины
    property_ids = list(cart.keys())
    properties = Property.objects.filter(pk__in=property_ids, is_available=True)
    
    # Подготавливаем данные для отображения
    cart_items = []
    total_price = Decimal('0')
    
    for prop in properties:
        quantity = cart.get(str(prop.pk), 1)
        subtotal = prop.price * quantity
        total_price += subtotal
        
        cart_items.append({
            'property': prop,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    # Конвертация общей суммы в валюты
    total_usd = CurrencyService.convert_to_usd(total_price) if total_price > 0 else 0
    total_eur = CurrencyService.convert_to_eur(total_price) if total_price > 0 else 0
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_usd': total_usd,
        'total_eur': total_eur,
        'cart_count': len(cart_items),
    }
    
    return render(request, 'realty/cart.html', context)


def add_to_cart(request, pk):
    """Добавление товара в корзину"""
    property_obj = get_object_or_404(Property, pk=pk, is_available=True)
    
    # Получаем или создаем корзину в сессии
    cart = request.session.get('cart', {})
    
    # Добавляем или увеличиваем количество
    property_key = str(pk)
    cart[property_key] = cart.get(property_key, 0) + 1
    
    # Сохраняем корзину в сессии
    request.session['cart'] = cart
    request.session.modified = True
    
    messages.success(request, f'"{property_obj.title}" добавлен в корзину!')
    
    # Возвращаемся на предыдущую страницу или на список
    return redirect(request.META.get('HTTP_REFERER', 'realty:property_list'))


def remove_from_cart(request, pk):
    """Удаление товара из корзины"""
    cart = request.session.get('cart', {})
    property_key = str(pk)
    
    if property_key in cart:
        del cart[property_key]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'Объект удален из корзины')
    
    return redirect('realty:cart')


def clear_cart(request):
    """Очистка корзины"""
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, 'Корзина очищена')
    return redirect('realty:cart')


def payment_view(request):
    """Страница оплаты"""
    # Получаем корзину из сессии
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('realty:cart')
    
    # Получаем объекты недвижимости из корзины
    property_ids = list(cart.keys())
    properties = Property.objects.filter(pk__in=property_ids, is_available=True)
    
    # Подсчитываем общую сумму
    total_price = Decimal('0')
    for prop in properties:
        quantity = cart.get(str(prop.pk), 1)
        total_price += prop.price * quantity
    
    if request.method == 'POST':
        # Обработка формы оплаты
        messages.success(request, 'Заказ успешно оформлен! Наш менеджер свяжется с вами.')
        
        # Очищаем корзину
        request.session['cart'] = {}
        request.session.modified = True
        
        return redirect('realty:home')
    
    context = {
        'properties': properties,
        'total_price': total_price,
        'cart': cart,
    }
    
    return render(request, 'realty/payment.html', context)


def faq_list(request):
    """Список часто задаваемых вопросов"""
    faqs = FAQ.objects.all().order_by('-added_at')

    # Поиск по вопросам
    query = request.GET.get('q')
    if query:
        faqs = faqs.filter(
            Q(question__icontains=query) |
            Q(answer__icontains=query)
        )

    context = {
        'faqs': faqs,
        'query': query,
    }

    return render(request, 'realty/faq_list.html', context)


def faq_detail(request, pk):
    """Детальная страница вопроса"""
    faq = get_object_or_404(FAQ, pk=pk)

    # Похожие вопросы
    related_faqs = FAQ.objects.exclude(pk=pk)[:5]

    context = {
        'faq': faq,
        'related_faqs': related_faqs,
    }

    return render(request, 'realty/faq_detail.html', context)