from django.db.models import Avg, Count, Sum, Max, Min, Q
from django.db.models.functions import TruncMonth, TruncDay
from decimal import Decimal
from statistics import median, mode, mean
from .models import Property, Sale, Buyer, Agent, Review, News
import json


class RealtyStatistics:
    """Класс для расчета статистики по недвижимости"""
    
    @staticmethod
    def get_properties_statistics():
        """Общая статистика по объектам недвижимости"""
        properties = Property.objects.filter(is_available=True)
        
        if not properties.exists():
            return {
                'total_count': 0,
                'avg_price': 0,
                'median_price': 0,
                'avg_area': 0,
                'type_distribution': {}
            }
        
        prices = list(properties.values_list('price', flat=True))
        areas = list(properties.values_list('area', flat=True))
        
        # Распределение по типам
        type_distribution = properties.values('property_type').annotate(
            count=Count('id'),
            avg_price=Avg('price'),
            total_value=Sum('price')
        ).order_by('-count')
        
        # Самый популярный тип
        most_popular_type = type_distribution.first() if type_distribution else None
        
        return {
            'total_count': properties.count(),
            'avg_price': float(properties.aggregate(Avg('price'))['price__avg'] or 0),
            'median_price': float(median(prices)) if prices else 0,
            'min_price': float(min(prices)) if prices else 0,
            'max_price': float(max(prices)) if prices else 0,
            'avg_area': float(mean(areas)) if areas else 0,
            'median_area': float(median(areas)) if areas else 0,
            'type_distribution': list(type_distribution),
            'most_popular_type': most_popular_type,
            'total_value': float(sum(prices))
        }
    
    @staticmethod
    def get_sales_statistics():
        """Статистика по продажам"""
        sales = Sale.objects.all()
        
        if not sales.exists():
            return {
                'total_sales': 0,
                'total_revenue': 0,
                'avg_sale_price': 0,
                'sales_by_month': []
            }
        
        # Продажи по месяцам
        sales_by_month = sales.annotate(
            month=TruncMonth('sale_date')
        ).values('month').annotate(
            count=Count('id'),
            revenue=Sum('price_with_discount')
        ).order_by('month')
        
        # Статистика по агентам
        agent_stats = sales.values('agent__user__first_name', 'agent__user__last_name').annotate(
            sales_count=Count('id'),
            total_revenue=Sum('price_with_discount')
        ).order_by('-sales_count')
        
        sale_prices = list(sales.values_list('price_with_discount', flat=True))
        
        return {
            'total_sales': sales.count(),
            'total_revenue': float(sales.aggregate(Sum('price_with_discount'))['price_with_discount__sum'] or 0),
            'avg_sale_price': float(mean(sale_prices)) if sale_prices else 0,
            'median_sale_price': float(median(sale_prices)) if sale_prices else 0,
            'sales_by_month': list(sales_by_month),
            'top_agents': list(agent_stats[:5])
        }
    
    @staticmethod
    def get_buyer_statistics():
        """Статистика по покупателям"""
        buyers = Buyer.objects.all()
        
        if not buyers.exists():
            return {
                'total_buyers': 0,
                'avg_budget': 0,
                'age_distribution': []
            }
        
        # Возрастное распределение
        from datetime import date
        today = date.today()
        
        age_groups = {
            '18-25': 0,
            '26-35': 0,
            '36-45': 0,
            '46-55': 0,
            '56+': 0
        }
        
        for buyer in buyers:
            if buyer.user.birth_date:
                age = today.year - buyer.user.birth_date.year
                if age <= 25:
                    age_groups['18-25'] += 1
                elif age <= 35:
                    age_groups['26-35'] += 1
                elif age <= 45:
                    age_groups['36-45'] += 1
                elif age <= 55:
                    age_groups['46-55'] += 1
                else:
                    age_groups['56+'] += 1
        
        budgets = list(buyers.exclude(budget__isnull=True).values_list('budget', flat=True))
        
        return {
            'total_buyers': buyers.count(),
            'avg_budget': float(mean(budgets)) if budgets else 0,
            'median_budget': float(median(budgets)) if budgets else 0,
            'age_distribution': [{'age_group': k, 'count': v} for k, v in age_groups.items()],
            'buyers_with_purchases': buyers.filter(sale__isnull=False).count()
        }
    
    @staticmethod
    def get_review_statistics():
        """Статистика по отзывам"""
        reviews = Review.objects.all()
        
        if not reviews.exists():
            return {
                'total_reviews': 0,
                'avg_rating': 0,
                'rating_distribution': []
            }
        
        rating_distribution = reviews.values('rating').annotate(
            count=Count('id')
        ).order_by('rating')
        
        ratings = list(reviews.values_list('rating', flat=True))
        
        return {
            'total_reviews': reviews.count(),
            'avg_rating': float(mean(ratings)) if ratings else 0,
            'median_rating': float(median(ratings)) if ratings else 0,
            'rating_distribution': list(rating_distribution),
            'recent_reviews': reviews.order_by('-created_at')[:5].values(
                'user__email', 'rating', 'text', 'created_at'
            )
        }
    
    @staticmethod
    def get_chart_data():
        """Данные для графиков"""
        properties = Property.objects.filter(is_available=True)
        
        # Данные для круговой диаграммы типов недвижимости
        type_data = properties.values('property_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        pie_chart_data = {
            'labels': [item['property_type'] for item in type_data],
            'data': [item['count'] for item in type_data]
        }
        
        # Данные для гистограммы цен
        price_ranges = {
            '0-50k': properties.filter(price__lt=50000).count(),
            '50k-100k': properties.filter(price__gte=50000, price__lt=100000).count(),
            '100k-200k': properties.filter(price__gte=100000, price__lt=200000).count(),
            '200k-300k': properties.filter(price__gte=200000, price__lt=300000).count(),
            '300k+': properties.filter(price__gte=300000).count(),
        }
        
        bar_chart_data = {
            'labels': list(price_ranges.keys()),
            'data': list(price_ranges.values())
        }
        
        # Данные для линейного графика продаж
        sales = Sale.objects.all().annotate(
            month=TruncMonth('sale_date')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        line_chart_data = {
            'labels': [item['month'].strftime('%Y-%m') if item['month'] else '' for item in sales],
            'data': [item['count'] for item in sales]
        }
        
        return {
            'pie_chart': pie_chart_data,
            'bar_chart': bar_chart_data,
            'line_chart': line_chart_data
        }
    
    @staticmethod
    def get_most_profitable_type():
        """Самый прибыльный тип недвижимости"""
        sales = Sale.objects.select_related('property').all()
        
        type_profits = {}
        for sale in sales:
            prop_type = sale.property.property_type
            if prop_type not in type_profits:
                type_profits[prop_type] = []
            type_profits[prop_type].append(float(sale.price_with_discount))
        
        if not type_profits:
            return None
        
        type_totals = {
            prop_type: {
                'total': sum(prices),
                'count': len(prices),
                'average': sum(prices) / len(prices) if prices else 0
            }
            for prop_type, prices in type_profits.items()
        }
        
        most_profitable = max(type_totals.items(), key=lambda x: x[1]['total'])
        
        return {
            'type': most_profitable[0],
            'total_profit': most_profitable[1]['total'],
            'sales_count': most_profitable[1]['count'],
            'average_price': most_profitable[1]['average']
        }