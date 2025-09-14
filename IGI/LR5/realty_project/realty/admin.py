from django.contrib import admin
from .models import Property, Owner, Buyer, Sale, Agent, CompanyInfo, FAQ, Vacancy, Review, PromoCode, News, Partner

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'price', 'owner', 'is_available')
    search_fields = ('title', 'address')
    list_filter = ('property_type', 'is_available')
    filter_horizontal = ('showing_agents',)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'passport')
    search_fields = ('user__email', 'passport')


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'budget')
    search_fields = ('user__email', 'phone')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('property', 'buyer', 'sale_date', 'contract_number')
    autocomplete_fields = ['property', 'buyer']




@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'phone')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description')
        }),
        ('Дополнительно', {
            'fields': ('logo', 'video_url', 'history', 'address', 'phone', 'email'),
            'classes': ('collapse',)
        })
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'added_at')
    search_fields = ('question', 'answer')
    date_hierarchy = 'added_at'
    fields = ('question', 'answer') 


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'department', 'experience_years', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'department')
    list_filter = ('department', 'is_active')
    autocomplete_fields = ['user']

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'is_published', 'published_at')
    search_fields = ('title',)
    list_filter = ('is_published',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('text', 'user__email')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'is_active', 'valid_to')
    search_fields = ('code',)
    list_filter = ('is_active', 'valid_to')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'is_published', 'views_count')
    search_fields = ('title', 'brief', 'content')
    list_filter = ('is_published', 'published_at')
    date_hierarchy = 'published_at'
    filter_horizontal = ('related_properties',)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'is_active', 'order')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)
    ordering = ('order', 'name')