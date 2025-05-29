from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, Buyer, Sale, Agent, CompanyInfo, FAQ, Vacancy, Review, PromoCode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from io import BytesIO
from django.contrib.auth.decorators import user_passes_test
import base64
from . import models
from django.db.models import Sum, Count, Avg
from collections import Counter
from datetime import datetime, date, timezone
from .forms import ReviewForm



def is_superuser(user):
    return user.is_superuser


def property_list(request):
    properties = Property.objects.filter(is_available=True).order_by('-created_at')

    query = request.GET.get('q')
    property_type = request.GET.get('type')

    if query:
        properties = properties.filter(title__icontains=query) | properties.filter(address__icontains=query)

    if property_type:
        properties = properties.filter(property_type=property_type)

    context = {
        'properties': properties,
        'query': query,
        'types': Property.PROPERTY_TYPES,
        'selected_type': property_type,
    }

    return render(request, 'propertys/property_list.html', context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'propertys/property_detail.html', {'property': property})



@login_required
def buy_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    try:
        buyer = Buyer.objects.get(user=request.user)
    except Buyer.DoesNotExist:
        messages.error(request, "Вы не зарегистрированы как покупатель")
        return redirect('realty:property_detail', pk=pk)

    if not prop.is_available:
        messages.warning(request, "Этот объект уже продан")
        return redirect('realty:property_detail', pk=pk)

    # Обработка промокода
    promo_code_str = request.GET.get('promo', None)
    final_price = prop.price

    promo = None
    if promo_code_str:
        try:
            promo = PromoCode.objects.get(code=promo_code_str, is_active=True)
            if promo.can_use():
                final_price *= (100 - promo.discount_percent) / 100
                promo.used_count += 1
                if promo.used_count >= promo.uses:
                    promo.is_active = False
                promo.save()
            else:
                messages.warning(request, "Промокод истёк или больше не действует")
        except PromoCode.DoesNotExist:
            messages.error(request, "Промокод не найден")

    # Создание сделки
    Sale.objects.create(
        property=prop,
        buyer=buyer,
        price_with_discount=final_price,
        contract_number=f"CON-{Sale.objects.count() + 1}-{prop.id}"
    )

    prop.is_available = False
    prop.save()

    messages.success(request, f"Вы купили {prop.title} со скидкой: {final_price}")
    return redirect('realty:property_detail', pk=pk)



@user_passes_test(is_superuser)
def statistics(request):
    # Базовые данные
    total_properties = Property.objects.count()
    total_sales = Sale.objects.count()

    # Общая сумма сделок
    total_income = Sale.objects.aggregate(total=Sum('property__price'))['total'] or 0

    # Средняя цена проданной недвижимости
    avg_price = Property.objects.filter(is_available=False).aggregate(avg_price=Avg('price'))['avg_price'] or 0

    # Типы недвижимости + общая сумма по типам
    property_types = Property.objects.values_list('property_type', flat=True)
    type_counter = Counter(property_types)
    most_common_type_code = type_counter.most_common(1)[0][0] if type_counter else None
    most_common_type = dict(Property.PROPERTY_TYPES).get(most_common_type_code, 'Нет данных')

    # Статистика по сотрудникам
    agent_stats = []
    for agent in Agent.objects.all():
        sales_count = Sale.objects.filter(property__agent=agent).count()
        income = Sale.objects.filter(property__agent=agent).aggregate(Sum('property__price'))['property__price__sum'] or 0
        avg_deal = Sale.objects.filter(property__agent=agent).aggregate(Avg('property__price'))['property__price__avg'] or 0

        agent_stats.append({
            'name': str(agent.user.full_name),
            'sales': sales_count,
            'income': income,
            'avg_deal': avg_deal
        })

    # График: типы недвижимости (вертикальная столбчатая диаграмма)
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    if not type_counter:
        ax1.text(0.5, 0.5, 'Нет данных', ha='center')
    else:
        types = [dict(Property.PROPERTY_TYPES).get(code, code) for code in type_counter.keys()]
        counts = list(type_counter.values())
        ax1.bar(types, counts, color='skyblue')
        ax1.set_title("Распределение объектов по типам")
        ax1.set_xlabel("Тип недвижимости")
        ax1.set_ylabel("Количество")

    buf1 = BytesIO()
    plt.savefig(buf1, format='png')
    plt.close(fig1)
    chart_property_types = base64.b64encode(buf1.getvalue()).decode('utf-8')

    # 🛠 Новая часть: круговая диаграмма по типам недвижимости на основе сделок
    sale_type_counter = Counter(
        Sale.objects.select_related('property').values_list('property__property_type', flat=True)
    )

    fig2, ax2 = plt.subplots(figsize=(8, 8))
    labels = [dict(Property.PROPERTY_TYPES).get(k, k) for k in sale_type_counter]
    sizes = list(sale_type_counter.values())

    if sum(sizes) == 0:
        ax2.text(0.5, 0.5, 'Нет данных о продажах по типам', ha='center', va='center')
    else:
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax2.axis('equal')  # чтобы получился круг
        ax2.set_title("Процент проданных объектов по типам")

    buf2 = BytesIO()
    plt.savefig(buf2, format='png')
    plt.close(fig2)
    chart_sale_by_type = base64.b64encode(buf2.getvalue()).decode('utf-8')

    # Диаграмма по сотрудникам
    agent_names = [a['name'] for a in agent_stats]
    agent_sales = [a['sales'] for a in agent_stats]

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    if not agent_sales:
        ax3.text(0.5, 0.5, 'Нет данных о сотрудниках', ha='center', va='center')
    else:
        ax3.bar(agent_names, agent_sales, color='lightgreen')
        ax3.set_title("Число сделок на сотрудника")
        ax3.tick_params(axis='x', rotation=45)

    buf3 = BytesIO()
    plt.savefig(buf3, format='png')
    plt.close(fig3)
    chart_agents = base64.b64encode(buf3.getvalue()).decode('utf-8')

    context = {
        'total_properties': total_properties,
        'total_sales': total_sales,
        'total_income_sum': total_income,
        'most_common_type': most_common_type,
        'avg_price': avg_price,
        'chart_property_types': chart_property_types,
        'chart_sale_by_type': chart_sale_by_type,   # ✅ новая диаграмма
        'chart_agents': chart_agents,
        'agent_stats': agent_stats,
    }

    return render(request, 'propertys/statistics.html', context)



def home(request):
    new_properties = Property.objects.order_by('-created_at')[:5]
    sold_properties = Sale.objects.select_related('property').order_by('-sale_date')[:5]

    events = []

    for prop in new_properties:
        events.append({
            'type': 'new_property',
            'title': f'Добавлен {prop.get_property_type_display()}',
            'description': f'Объект "{prop.title}" добавлен в каталог.',
            'date': prop.created_at,
        })

    for sale in sold_properties:
        # Если sale.sale_date - это date, преобразуем его в datetime
        sale_datetime = datetime.combine(sale.sale_date, datetime.min.time(), tzinfo=timezone.utc)

        events.append({
            'type': 'sold',
            'title': f'Продан {sale.property.get_property_type_display()}',
            'description': f'{sale.property.title} был куплен {sale.buyer.user.full_name if sale.buyer else "неизвестным покупателем"}',
            'date': sale_datetime,
        })

    # Сортируем события по дате
    events.sort(key=lambda x: x['date'], reverse=True)
    latest_events = events[:5]

    return render(request, 'home.html', {'events': latest_events})


def about(request):
    info = CompanyInfo.objects.first() or CompanyInfo.objects.create(title="Наше агентство", description="Контент будет позже")
    return render(request, 'about.html', {'info': info})


def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq_list.html', {'faqs': faqs})


def contact_list(request):
    agents = Agent.objects.filter(is_active=True).select_related('user')
    return render(request, 'contacts.html', {'agents': agents})

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def vacancy_list(request):
    vacancies = Vacancy.objects.filter(is_published=True)
    return render(request, 'vacancies/vacancy_list.html', {'vacancies': vacancies})


def reviews_list(request):
    reviews = Review.objects.select_related('user').all()
    return render(request, 'reviews/list.html', {'reviews': reviews})


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('reviews_list')
    else:
        form = ReviewForm()

    return render(request, 'reviews/form.html', {'form': form})


def promo_list(request):
    promos = PromoCode.objects.filter(is_active=True)
    return render(request, 'promo/list.html', {'promos': promos})